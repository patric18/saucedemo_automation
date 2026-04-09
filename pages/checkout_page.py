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
    ERROR_CONTAINER = (By.CSS_SELECTOR, "[data-test='error']")

    def wait_for_step_one(self, timeout=45):
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(self.STEP_ONE_CONTAINER)
        )

    def wait_for_step_two(self, timeout=45):
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(self.STEP_TWO_CONTAINER)
        )

    def fill_form(self, firstname, lastname, postalcode):
        # petarede way: JS + input events, wait na każdy input
        for locator, value, name in [
            (self.FIRST_NAME, firstname, "FIRST"),
            (self.LAST_NAME, lastname, "LAST"),
            (self.POSTAL_CODE, postalcode, "CODE"),
        ]:
            input_field = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(locator)
            )
            self.driver.execute_script("""
                arguments[0].focus();
                arguments[0].value = arguments[1];
                arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
            """, input_field, value)

            # czekamy aż wartość inputu będzie faktycznie w DOM
            WebDriverWait(self.driver, 2).until(
                lambda d: input_field.get_attribute('value') == value
            )
            print(f"{name} -> expected: '{value}' | actual: '{input_field.get_attribute('value')}'")

    def continue_checkout(self, wait_for_step_two=True):
        continue_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.CONTINUE_BTN)
        )
        # scroll i JS click
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", continue_btn)
        self.driver.execute_script("arguments[0].click();", continue_btn)

        if wait_for_step_two:
            WebDriverWait(self.driver, 10).until(
                lambda d: "checkout-step-two" in d.current_url or d.find_elements(*self.ERROR_CONTAINER)
            )
            if "checkout-step-two" not in self.driver.current_url:
                raise Exception(f"Did not navigate to Step Two. Current URL: {self.driver.current_url}")
             
    def finish(self):
        self.click(self.FINISH_BTN)

    def get_success_message(self):
        return self.get_text(self.SUCCESS_MSG)

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
    
    def get_error_message(self):
        return self.driver.find_element(By.CSS_SELECTOR, "[data-test='error']").text