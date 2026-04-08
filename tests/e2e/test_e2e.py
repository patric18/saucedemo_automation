from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CheckoutPage(BasePage):
    FIRST_NAME = (By.ID, "first-name")
    LAST_NAME = (By.ID, "last-name")
    POSTAL_CODE = (By.ID, "postal-code")
    CONTINUE_BTN = (By.ID, "continue")
    FINISH_BTN = (By.ID, "finish")
    SUCCESS_MSG = (By.CLASS_NAME, "complete-header")
    STEP_ONE_CONTAINER = (By.ID, "checkout-info-container")
    STEP_TWO_CONTAINER = (By.ID, "checkout_summary_container")

    def fill_form(self, first, last, code):
        self.type(self.FIRST_NAME, first)
        self.type(self.LAST_NAME, last)
        self.type(self.POSTAL_CODE, code)

    def continue_checkout(self):
        self.click(self.CONTINUE_BTN)
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_all_elements_located(self.STEP_TWO_CONTAINER)
        )

    def finish(self):
        self.click(self.FINISH_BTN)
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_all_elements_located(self.SUCCESS_MSG)
        )

    def get_success_message(self):
        return self.get_text(self.SUCCESS_MSG)

    def is_step_one_loaded(self, timeout=30):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located(self.STEP_ONE_CONTAINER)
            )
            return True
        except:
            return False

    def is_step_two_loaded(self, timeout=30):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located(self.STEP_TWO_CONTAINER)
            )
            return True
        except:
            return False