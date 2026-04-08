import pytest
from selenium import webdriver
import os
from datetime import datetime
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import prefs

def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # bez okna
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    return driver


@pytest.fixture
def driver():
    opts = Options()
    opts.add_experimental_option("prefs",{
        "credentials_ennable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False
    })
    #driver = webdriver.Chrome(service=Service, options=chrome_options(ChromeDriverManager().install()))
    driver = webdriver.Chrome(options=opts)
    driver.maximize_window()
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