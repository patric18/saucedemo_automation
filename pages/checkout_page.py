from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class CheckoutPage(BasePage):
    FIRST_NAME = (By.ID, "first-name")
    LAST_NAME = (By.ID, "last-name")
    POSTAL_CODE = (By.ID, "postal-code")
    CONTINUE_BTN = (By.ID, "continue")
    FINISH_BTN = (By.ID, "finish")
    SUCCESS_MSG = (By.CLASS_NAME, "complete-header")
    ERROR = (By.CSS_SELECTOR, "h3[data-test='error']")

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
    
    def get_error(self):
        return self.get_text(self.ERROR)