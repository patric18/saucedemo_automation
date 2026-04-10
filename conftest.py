import pytest
from selenium import webdriver
import os
from datetime import datetime
from selenium.webdriver.chrome.options import Options
#import prefs
from selenium.webdriver.chrome.service import Service


""" Chrome setups 
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

"""

@pytest.fixture
def driver():
    options = Options()
    
    # Headless nowy tryb w Chrome >= 109
    options.add_argument("--headless=new")  
    options.add_argument("--disable-gpu")
    options.add_argument("--log-level=3")
    options.add_argument("--silent")
    options.add_argument("--window-size=1920,1080")  # rozmiar okna
    options.add_argument("--disable-logging")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    
    # jeśli chcesz logi w Chrome
    # options.add_argument("--enable-logging")
    # options.add_argument("--v=1")
    
    driver = webdriver.Chrome(options=options)
    
    
    yield driver
    driver.quit()

@pytest.fixture(autouse=True)
def clean_state(driver):
    driver.get("https://www.saucedemo.com/")
    driver.delete_all_cookies()
    driver.execute_script("window.localStorage.clear();")
    driver.execute_script("window.sessionStorage.clear();")


# screenshot on fail
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            os.makedirs("artifacts", exist_ok=True)

            name = f"{item.name}_{datetime.now().strftime('%H-%M-%S')}"

            driver.save_screenshot(f"artifacts/{name}.png")

            with open(f"artifacts/{name}.html", "w") as f:
                f.write(driver.page_source)

            with open(f"artifacts/{name}.txt", "w") as f:
                f.write(driver.current_url)

