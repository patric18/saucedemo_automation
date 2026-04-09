import time

from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

class CheckoutPage(BasePage):
    STEP_ONE_CONTAINER = (By.ID, "checkout_info_container")
    STEP_TWO_CONTAINER = (By.ID, "checkout_summary_container")
    FIRST_NAME = (By.ID, "first-name")
    LAST_NAME = (By.ID, "last-name")
    POSTAL_CODE = (By.ID, "postal-code")
    CONTINUE_BTN = (By.ID, "continue")
    FINISH_BTN = (By.ID, "finish")
    SUCCESS_MSG = (By.CLASS_NAME, "complete-header")
    ERROR_MSG = (By.CSS_SELECTOR, "[data-test='error']")

    def wait_for_step_one(self, timeout=10):
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(self.STEP_ONE_CONTAINER)
        )

    def wait_for_step_two(self, timeout=10):
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(self.STEP_TWO_CONTAINER)
        )

    def fill_form(self, firstname, lastname, postalcode):
        fields = [
            (self.FIRST_NAME, firstname),
            (self.LAST_NAME, lastname),
            (self.POSTAL_CODE, postalcode),
        ]

        for locator, value in fields:
            field = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(locator)
            )
            field.clear()
            field.send_keys(value)

            # Czekamy aż React/JS zapisze wartość w input
            WebDriverWait(self.driver, 2).until(
                lambda d: field.get_attribute("value") == value
            )

        # Debug
        print("FIRST -> expected:", firstname, "| actual:", self.driver.find_element(*self.FIRST_NAME).get_attribute("value"))
        print("LAST  -> expected:", lastname,  "| actual:", self.driver.find_element(*self.LAST_NAME).get_attribute("value"))
        print("CODE  -> expected:", postalcode,"| actual:", self.driver.find_element(*self.POSTAL_CODE).get_attribute("value"))
        print("Checkout form values:", firstname, lastname, postalcode)

    def continue_checkout(self, wait_for_step_two=True):
        continue_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.CONTINUE_BTN)
        )

        # JS click
        self.driver.execute_script("arguments[0].click();", continue_btn)

        if wait_for_step_two:
            # Czekamy aż URL zmieni się na step-two lub pojawi się błąd
            WebDriverWait(self.driver, 10).until(
                lambda d: "checkout-step-two" in d.current_url or d.find_elements(By.CLASS_NAME, "error-message-container")
            )

            if "checkout-step-two" not in self.driver.current_url:
                raise Exception(f"Did not navigate to Step Two. Current URL: {self.driver.current_url}")

    def finish(self):
        finish_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.FINISH_BTN)
        )
        self.driver.execute_script("arguments[0].click();", finish_btn)

    def get_success_message(self):
        return WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located(self.SUCCESS_MSG)
        ).text

    def get_error_message(self):
        return WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located(self.ERROR_MSG)
        ).text

    def is_step_one_loaded(self):
        try:
            WebDriverWait(self.driver, 10).until(
                lambda d: "checkout-step-one" in d.current_url
            )
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.STEP_ONE_CONTAINER)
            )
            return True
        except:
            print("FAILED STEP ONE, URL:", self.driver.current_url)
            return False

    def is_step_two_loaded(self):
        try:
            WebDriverWait(self.driver, 10).until(
                lambda d: "checkout-step-two" in d.current_url
            )
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.STEP_TWO_CONTAINER)
            )
            return True
        except:
            print("FAILED STEP TWO, URL:", self.driver.current_url)
            return False