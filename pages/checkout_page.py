import time
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

    def wait_for_step_one(self, timeout=10):
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(self.STEP_ONE_CONTAINER)
        )

    def wait_for_step_two(self, timeout=10):
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(self.STEP_TWO_CONTAINER)
        )

    def fill_form(self, firstname, lastname, postalcode):
        wait = WebDriverWait(self.driver, 10)

        first = wait.until(EC.presence_of_element_located(self.FIRST_NAME))
        last = wait.until(EC.presence_of_element_located(self.LAST_NAME))
        code = wait.until(EC.presence_of_element_located(self.POSTAL_CODE))

        # 🔥 FIRST NAME
        first.clear()
        first.send_keys(firstname)

        wait.until(lambda d: first.get_attribute("value") == firstname)

        # 🔥 LAST NAME
        last.clear()
        last.send_keys(lastname)

        wait.until(lambda d: last.get_attribute("value") == lastname)

        # 🔥 POSTAL CODE
        code.clear()
        code.send_keys(postalcode)

        wait.until(lambda d: code.get_attribute("value") == postalcode)

        print("VALUES:", 
            first.get_attribute("value"),
            last.get_attribute("value"),
            code.get_attribute("value"))

    def continue_checkout(self, wait_for_step_two=True):
        continue_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.CONTINUE_BTN)
        )

        continue_btn.click()

        if wait_for_step_two:
            WebDriverWait(self.driver, 10).until(
                lambda d: "checkout-step-two" in d.current_url or d.find_elements(*self.ERROR_CONTAINER)
            )

    def finish(self):
        finish_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.FINISH_BTN)
        )
        self.driver.execute_script("arguments[0].click();", finish_btn)

    def get_success_message(self):
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.SUCCESS_MSG)
        ).text

    def is_step_one_loaded(self):
        try:
            self.wait_for_step_one()
            return True
        except:
            print("FAILED STEP ONE, URL:", self.driver.current_url)
            return False

    def is_step_two_loaded(self):
        try:
            self.wait_for_step_two()
            return True
        except:
            print("FAILED STEP TWO, URL:", self.driver.current_url)
            return False

    def get_error_message(self):
        return WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located(self.ERROR_CONTAINER)
        ).text