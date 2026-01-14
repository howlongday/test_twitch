Twitch Mobile Web Automation (Pytest + Selenium)
This project is a robust automation suite designed for testing the Twitch Mobile Web interface. Built with Python, Pytest, and Selenium, it features mobile device emulation, self-healing popup management, and detailed reporting with automated screenshots.

📸 Demo
(Replace this with your actual Demo.gif path if hosted on GitHub/GitLab)

✨ Key Features
Mobile Emulation: Automatically simulates a Google Pixel 7 environment using Chrome DevTools Protocol.

Self-Healing Popup Handler: Built-in logic in actions.py to detect and dismiss intrusive UI elements (e.g., cookie banners, "Muted Content" alerts) during execution.

Automated Step-by-Step Screenshots:

Captures screenshots for every critical action, saved in screenshots/{timestamp}/{test_name}/.

Failure Snapshot: Automatically triggers a full-page screenshot upon test failure via Pytest hooks.

Interactive Reports: Generates a self-contained HTML report with execution details and embedded logs.

📂 Project Structure
Plaintext

pytest/
├── testcases/            # Test scenario implementations
│   └── test_twitch.py    # Main test script (Search, Scroll, and Playback)
├── actions.py            # Custom wrapper for Selenium (Page Object Pattern)
├── conftest.py           # Pytest fixtures (Browser setup, Screenshot hooks)
├── constants.py          # Shared UI selectors and configuration constants
├── requirements.txt      # Project dependencies
├── run_test.bat          # Batch script for one-click execution (Windows)
├── .gitignore            # Git exclusion rules
└── report.html           # Generated test report (Post-execution)
🛠️ Setup & Installation
1. Prerequisites
Python 3.8+

Google Chrome Browser

2. Install Dependencies
Open your terminal and run:

Bash

pip install -r requirements.txt
3. Run the Tests
You can execute the tests using either of the following methods:

Option A: Batch Script (Windows) Double-click run_test.bat. This will automatically install missing packages and trigger the test suite.

Option B: Command Line

Bash

pytest -vs --html=report.html --self-contained-html
📊 Results & Artifacts
HTML Report: Open report.html in any browser to view the test summary.

Screenshots: Check the screenshots/ directory for chronological captures of the test flow.

📝 Test Workflow (Twitch Search)
Initialize: Navigate to Twitch Mobile and clear initial popups.

Search: Click the search icon and input "StarCraft II".

Filter: Navigate to the "Channels" tab.

Browse: Perform a vertical scroll (x2) to load dynamic content.

Selection: Randomly select a live streamer from the results.

Validation: Wait for the video player to load, verify playback state, and take a final confirmation screenshot.