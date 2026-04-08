import pytest
from selenium import webdriver
import os
from datetime import datetime
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import prefs
from selenium.webdriver.chrome.service import Service

@pytest.fixture
def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    service = Service(ChromeDriverManager().install())  # <--- używamy Service
    driver = webdriver.Chrome(service=service, options=options)  # <--- podajemy service i options
    yield driver
    driver.quit()




# screenshot on fail
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")

        if driver:
            os.makedirs("screenshots", exist_ok=True)
            file_name = f"{item.name}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.png"
            driver.save_screenshot(f"screenshots/{file_name}")