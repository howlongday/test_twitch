# Twitch Mobile Web Automation (Pytest + Selenium)

This project implements UI automation testing for the Twitch mobile website using Python and Pytest. It includes features such as mobile device emulation, automated popup handling, and screenshot logging.

## 📸 Demo
<img src="./Demo.gif" width="400">

## ✨ Key Features
- Mobile Emulation: Automatically simulates a Google Pixel 7 environment using Chrome DevTools Protocol.
- Self-Healing Popup Handler: Built-in logic in actions.py to detect and dismiss intrusive UI elements during execution.
- Automated Screenshots:
  - Failure Snapshot: Automatically triggers a full-page screenshot upon test failure via Pytest hooks.
- Interactive Reports: Generates a self-contained HTML report with execution details and embedded logs.

## 📂 Project Structure
```text
pytest/
├── testcases/            # Test scenario implementations
│   └── test_twitch.py    # Main test script (Search, Scroll, and Playback)
├── actions.py            # Custom wrapper for Selenium (Page Object Pattern)
├── conftest.py           # Pytest fixtures (Browser setup, Screenshot hooks)
├── constants.py          # Shared UI selectors and configuration constants
├── requirements.txt      # Project dependencies
├── run_test.bat          # Batch script for one-click execution (Windows)
└── .gitignore            # Git exclusion rules
```

## 🛠️ Setup & Installation

1. Prerequisites
- Python 3.8+
- Google Chrome Browser

2. Install Dependencies
Open your terminal and run:
```text
pip install -r requirements.txt
```

4. Run the Tests
You can execute the tests using either of the following methods:

- Option A: Batch Script (Windows)
  Double-click run_test.bat. This will automatically install missing packages and trigger the test suite.
- Option B: Command Line
 ```text
  pytest -vs --html=report.html --self-contained-html
  ```

## 📊 Results & Artifacts
- HTML Report: Open report.html in any browser to view the test summary.
- Screenshots: Check the screenshots/ directory for chronological captures of the test flow.

## 📝 Test Workflow (Twitch Search)
1. Initialize: Navigate to Twitch Mobile and clear initial popups.
2. Search: Click the search icon and input "StarCraft II".
3. Filter: Navigate to the "Channels" tab.
4. Browse: Perform a vertical scroll (x2) to load dynamic content.
5. Selection: Randomly select a live streamer from the results.
6. Validation: Wait for the video player to load, verify playback state, and take a final confirmation screenshot.
