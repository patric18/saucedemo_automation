![Tests](https://github.com/YOUR_USERNAME/YOUR_REPO/actions/workflows/tests.yml/badge.svg)

# SauceDemo Automation

> Automated testing framework for the SauceDemo e-commerce site using **Python** and **pytest**.  
> 22 fully functional end-to-end tests covering core user flows.

---

## Project Overview
This project is a practical automation suite for [SauceDemo](https://www.saucedemo.com), designed to test key e-commerce functionalities.  
The framework follows the **Page Object Model**, keeping tests organized, reusable, and easy to maintain.

### Key Scenarios Covered

- ✅ User login (valid and invalid credentials)  
- ✅ Adding and removing items from the shopping cart  
- ✅ Checkout process  
- ✅ Error handling and validation scenarios  

With **22 automated tests**, this suite ensures that the main flows of SauceDemo are thoroughly tested.

---

## Features

- 22 fully working end-to-end tests  
- Automatic **screenshots on test failure** (saved in `/screenshots`)  
- Modular **Page Object Pattern** design  
- Reusable fixtures for browser setup and teardown (`conftest.py`)  
- Easy local execution with **pytest**  
- Designed for maintainability and clarity  

---

## SCREENSHOTS

Screenshots for failed tests are automatically saved in /screenshots. Browser options can be adjusted in conftest.py.


## Future Improvements
Integrate CI/CD using GitHub Actions
Generate Allure or HTML reports for test results
Add cross-browser and data-driven testing using parameterized tests
Expand test coverage for more edge cases

## Installation

1. Clone the repository:

```bash
git clone https://github.com/patric18/saucedemo_automation.git
cd saucedemo_automation

2. Install dependencies:
pip install -r requirements.txt

3. Running Tests
Run all tests:
python -m pytest -v --capture=tee-sys

Run a specific test file:
python -m pytest -v tests/login/test_login.py

PROJECT STRUCTURE
saucedemo_automation/
├── pages/           # Page Object classes – representations of app pages
├── tests/           # Main folder containing all test scenarios
│   ├── login/       # Tests for login functionality
│   ├── cart/        # Tests for shopping cart operations
│   ├── checkout/    # Tests for checkout process
│   ├── inventory/    # Tests for product listing and sorting
│   └── e2e/         # Tests e2e
│   
├── utils/           # Helper functions (data generators, utilities)
├── screenshots/     # Screenshots for failed tests
├── conftest.py      # Pytest fixtures (setup/teardown)
├── requirements.txt # Python dependencies
└── README.md        # Project documentation