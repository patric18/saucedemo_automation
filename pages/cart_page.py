from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CartPage(BasePage):

    CART_ITEMS = (By.CLASS_NAME, "cart_item")
    CHECKOUT_BTN = (By.ID, "checkout")
    CART_CONTAINER = (By.ID, "cart_contents_container")

    def wait_for_cart_loaded(self, timeout=20):
        WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(self.CART_ITEMS)
        )

    def get_items_count(self):
        self.wait_for_cart_loaded()
        return len(self.find_all(self.CART_ITEMS))
    
    def go_to_checkout(self):
        self.wait_for_cart_loaded()
        self.click(self.CHECKOUT_BTN)

    def is_cart_empty(self):
        self.wait_for_cart_loaded()
        return len(self.driver.find_elements(self.CART_ITEMS))
    
    def remove_all_products(self):
        self.wait_for_cart_loaded()
        buttons = self.get_remove_buttons()
        for btn in buttons:
            btn.click()

    def is_loaded(self):
        try:
            self.wait_for_cart_loaded()
            return True
        except:
            return False            