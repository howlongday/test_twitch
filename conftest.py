import pytest
import os
from selenium import webdriver
from datetime import datetime

SESSION_START_TIME = datetime.now().strftime("%Y%m%d_%H%M%S")

@pytest.fixture(scope="session")
def base_path():
    """建立總目錄：screenshots/起始時間"""
    path = f"screenshots/{SESSION_START_TIME}"
    os.makedirs(path, exist_ok=True)
    return path

@pytest.fixture
def test_folder(base_path, request):
    """為每個測試函數建立獨立子目錄"""
    folder_path = os.path.join(base_path, request.node.name)
    os.makedirs(folder_path, exist_ok=True)
    return folder_path

@pytest.fixture
def browser():
    """啟動 Chrome 瀏覽器並設定手機模擬與視窗佈局"""
    mobile_emulation = { "deviceName": "Pixel 7" }
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--high-dpi-support=0")
    chrome_options.add_argument("--force-device-scale-factor=1.6")
    chrome_options.add_argument("--disable-blink-features=WebShare")
    chrome_options.add_argument("--window-size=855,1140")
    chrome_options.add_argument("--window-position=0,0")
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Pytest Hook: 當測試失敗時自動執行錯誤處理（截圖）。
    """
    outcome = yield
    rep = outcome.get_result()

    # 只有在執行階段發生錯誤時觸發
    if rep.when == "call" and rep.failed:
        if "browser" in item.funcargs:
            driver = item.funcargs["browser"]
            
            # 優先嘗試獲取該測試案例的專屬資料夾，若無則存於 error_screenshots
            target_dir = item.funcargs.get("test_folder", "error_screenshots")
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)
            
            timestamp = datetime.now().strftime('%H%M%S')
            file_name = os.path.join(target_dir, f"CRITICAL_FAILURE_{timestamp}.png")
            
            driver.save_screenshot(file_name)
            print(f"\n[Error Handling] Hook detected failure. Evidence saved to: {file_name}")