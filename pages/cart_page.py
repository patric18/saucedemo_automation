from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class CartPage(BasePage):

    CART_ITEMS = (By.CLASS_NAME, "cart_item")
    CHECKOUT_BTN = (By.ID, "checkout")

    def get_items_count(self):
        return len(self.find_all(self.CART_ITEMS))
    
    def go_to_checkout(self):
        self.click(self.CHECKOUT_BTN)

    def is_cart_empty(self):
        return len(self.driver.find_elements(self.CART_ITEMS))
    
    def remove_all_products(self):
        buttons = self.get_remove_buttons()
        for btn in buttons:
            btn.click()

    def is_loaded(self):
        return "cart" in self.driver.current_url            