from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class CheckoutPage(BasePage):
    FIRST_NAME = (By.ID, "first-name")
    LAST_NAME = (By.ID, "last-name")
    POSTAL_CODE = (By.ID, "postal-code")
    CONTINUE_BTN = (By.ID, "continue")
    FINISH_BTN = (By.ID, "finish")
    SUCCESS_MSG = (By.CLASS_NAME, "complete-header")
    ERROR = (By.CSS_SELECTOR, "h3[data-test='error']")
    STEP_ONE_CONTAINER = (By.ID, "checkout-info-container")

    def wait_for_step_one(self, timeout=10):
        """Wait until step one page is visible"""
        WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(self.STEP_ONE_CONTAINER)
        )

    def fill_form(self, first, last, code):
        self.wait_for_step_one()
        self.type(self.FIRST_NAME, first)
        self.type(self.LAST_NAME, last)
        self.type(self.POSTAL_CODE, code)

    def continue_checkout(self):
        self.click(self.CONTINUE_BTN)

    def finish(self):
        self.click(self.FINISH_BTN)

    def get_success_message(self):
        return self.get_text(self.SUCCESS_MSG)
    
    def get_error(self):
        try:
            return self.get_text(self.ERROR)
        except:
            return ""
        
    def is_step_one_loaded(self):
        return "checkout-step-one" in self.driver.current_url    
    
    def is_step_two_loaded(self):
        return "checkout-step-two" in self.driver.current_url   