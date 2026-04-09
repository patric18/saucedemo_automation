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

    def wait_for_step_one(self, timeout=45):
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(self.STEP_ONE_CONTAINER)
        )

    def wait_for_step_two(self, timeout=45):
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(self.STEP_TWO_CONTAINER)
        )

    def fill_form(self, firstname, lastname, postalcode):
        fields = [
            ("FIRST", self.FIRST_NAME, firstname),
            ("LAST", self.LAST_NAME, lastname),
            ("CODE", self.POSTAL_CODE, postalcode),
        ]

        for label, locator, value in fields:
            field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(locator)
            )
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});", field
            )
            field.click()
            field.clear()

            if value:
                field.send_keys(value)
                # JS fallback
                if field.get_attribute("value") != value:
                    self.driver.execute_script(
                        "arguments[0].value = arguments[1];", field, value
                    )

            # 🔍 Poczekaj aż value będzie widoczne w DOM
            WebDriverWait(self.driver, 2).until(
                lambda d: field.get_attribute("value") == value
            )

            actual = field.get_attribute("value")
            print(f"{label} -> expected: '{value}' | actual: '{actual}'")

    def continue_checkout(self, wait_for_step_two=True):
        continue_btn = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.CONTINUE_BTN)
        )

        # wait 0.2 sec for stabilizating inputs - this time.sleep repaired test..
        time.sleep(0.2)

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", continue_btn
        )
        time.sleep(0.1)

        self.driver.execute_script("arguments[0].click();", continue_btn)

        if wait_for_step_two:
            WebDriverWait(self.driver, 10).until(
                lambda d: (
                    "checkout-step-two" in d.current_url or
                    d.find_elements(By.CLASS_NAME, "error-message-container")
                )
            )
            if "checkout-step-two" not in self.driver.current_url:
                raise Exception(
                    f"Did not navigate to Step Two. Current URL: {self.driver.current_url}"
                )

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