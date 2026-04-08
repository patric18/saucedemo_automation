from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CheckoutPage(BasePage):
    STEP_ONE_CONTAINER = (By.ID, "checkout-info-container")
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

    def fill_form(self, first, last, code):
        self.type(self.FIRST_NAME, first)
        self.type(self.LAST_NAME, last)
        self.type(self.POSTAL_CODE, code)

    def continue_checkout(self):
        self.click(self.CONTINUE_BTN)

    def finish(self):
        self.click(self.FINISH_BTN)

    def get_success_message(self):
        return self.get_text(self.SUCCESS_MSG)

    def is_step_one_loaded(self):
        try:
            self.wait_for_step_one()
            return True
        except:
            return False

    def is_step_two_loaded(self):
        try:
            self.wait_for_step_two()
            return True
        except:
            return False