import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from constants import POPUP_SELECTORS

class MainActions:
    def __init__(self, browser, test_folder):
        """Initializes the action handler with browser instance and self-healing configurations."""
        self.browser = browser
        self.test_folder = test_folder
        self.wait = WebDriverWait(self.browser, 15)
        self.common_popups = POPUP_SELECTORS

    def _get_loc(self, selector):
        """Private helper to determine locator type (XPATH or CSS) based on selector string."""
        if selector.startswith('//') or selector.startswith('(') or selector.startswith('/'):
            return (By.XPATH, selector)
        return (By.CSS_SELECTOR, selector)

    def waitfor(self, selector):
        """Waits for an element to be visible with built-in self-healing for popups."""
        try:
            return self.wait.until(EC.visibility_of_element_located(self._get_loc(selector)))
        except:
            time.sleep(1)
            self.auto_handle_popups()
            return self.wait.until(EC.visibility_of_element_located(self._get_loc(selector)))

    def input_text(self, selector, text, press_enter=False):
        """Clears target input field and sends text, with optional ENTER key support."""
        element = self.waitfor(selector)
        element.clear()
        element.send_keys(text)
        if press_enter:
            element.send_keys(Keys.ENTER)

    def auto_handle_popups(self):
        """Executes JavaScript injection to scan and clear predefined UI popups/overlays."""
        selectors_json = str(self.common_popups)

        js_script = f"""
        var selectors = {selectors_json};
        selectors.forEach(selector => {{
            var el = document.querySelector(selector);
            if (el && el.offsetWidth > 0 && el.offsetHeight > 0) {{
                el.click();
            }}
        }});
        """
        try:
            self.browser.execute_script(js_script)
        except:
            pass

    def scroll(self, direction="down", times=2):
        """Performs smooth window scrolling via JavaScript in four possible directions."""
        top, left, pixels = 0, 0, 500
        if direction == "down": top = pixels
        elif direction == "up": top = -pixels
        elif direction == "right": left = pixels
        elif direction == "left": left = -pixels

        for _ in range(times):
            self.browser.execute_script(f"window.scrollBy({{top: {top}, left: {left}, behavior: 'smooth'}});")
            time.sleep(1)

    def take_screenshot(self, name):
        """Captures a timestamped screenshot of the current page for test verification."""
        timestamp = time.strftime("%H%M%S")
        filename = f"{self.test_folder}/{timestamp}_{name}.png"
        self.browser.save_screenshot(filename)

    def open_url(self, url):
        """Navigates to URL and blocks until the browser triggers 'document.readyState == complete'."""
        self.browser.get(url)
        self.wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
        time.sleep(1)
    
    def push_enter(self, selector, wait_selector=None):
        """Simulates physical ENTER key on a selector and optionally waits for subsequent UI response."""
        element = self.waitfor(selector)
        element.send_keys(Keys.ENTER)
        if wait_selector:
            self.waitfor(wait_selector)
        time.sleep(1)
        
    def click_and_wait(self, click_selector, wait_selector=None):
        """Clicks an interactable element and ensures synchronization by waiting for a target selector."""
        btn = self.wait.until(EC.element_to_be_clickable(self._get_loc(click_selector)))
        btn.click()
        if wait_selector:
            self.waitfor(wait_selector)
        time.sleep(1)
        
    def wait_until_gone(self, selector, timeout=10):
        """High-performance JS polling to verify an element is hidden or removed from the DOM."""
        start_time = time.time()
        while time.time() - start_time < timeout:
            is_gone = self.browser.execute_script(f"""
                var el = document.querySelector('{selector}');
                if (!el) return true; 
                var style = window.getComputedStyle(el);
                return (style.display === 'none' || style.visibility === 'hidden' || el.offsetWidth === 0);
            """)
            if is_gone:
                #print(f">>> [JS 確認] 載入元件已消失，耗時: {round(time.time() - start_time, 2)}s")
                return True           
            time.sleep(0.3)
        #print(f">>> 警告: {selector} 超時未消失，強制繼續執行下一步")
        return False