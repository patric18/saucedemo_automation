from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CartPage(BasePage):
    CART_CONTAINER = (By.ID, "cart_contents_container")
    CART_ITEMS = (By.CLASS_NAME, "cart_item")
    CHECKOUT_BTN = (By.ID, "checkout")

    def wait_for_cart_loaded(self, timeout=45):
        """Czekamy aż kontener koszyka pojawi się w DOM"""
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(self.CART_CONTAINER)
        )

    def get_items_count(self):
        self.wait_for_cart_loaded()
        return len(self.driver.find_elements(*self.CART_ITEMS))

    def is_loaded(self):
        try:
            self.wait_for_cart_loaded()
            return True
        except:
            return False

    def go_to_checkout(self):
        self.click(self.CHECKOUT_BTN)