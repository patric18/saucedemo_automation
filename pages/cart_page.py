from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CartPage(BasePage):
    CART_ITEMS = (By.CLASS_NAME, "cart_item")
    CHECKOUT_BTN = (By.ID, "checkout")
    CART_CONTAINER = (By.ID, "cart_contents_container")

    def wait_for_cart_loaded(self, timeout=30):
        """Czeka aż koszyk pojawi się w DOM (niekoniecznie widoczny)"""
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#cart_contents_container .cart_item, #cart_contents_container"))
        )

    def get_items_count(self):
        self.wait_for_cart_loaded()
        return len(self.driver.find_elements(*self.CART_ITEMS))

    def go_to_checkout(self):
        self.wait_for_cart_loaded()
        self.click(self.CHECKOUT_BTN)

    def is_loaded(self):
        try:
            self.wait_for_cart_loaded()
            return True
        except:
            return False