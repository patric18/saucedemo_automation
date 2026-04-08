from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class InventoryPage(BasePage):

    PRODUCTS = (By.CLASS_NAME, "inventory_item")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")

    def add_products(self, count):
        for _ in range(count):
        # wybierz pierwszy przycisk "Add to cart"
            btn = next(
                b for b in self.driver.find_elements(By.CLASS_NAME, "btn_inventory")
                if b.text.lower() == "add to cart"
            )
        # kliknij
            btn.click()

        # poczekaj aż badge zaktualizuje się o jeden element
            WebDriverWait(self.driver, 5).until(
                lambda d: int(self.get_cart_count()) >= _ + 1
            )
    
    def go_to_cart(self):
        self.click(self.CART_LINK)

        WebDriverWait(self.driver, 10).until(
            lambda d: "/cart.html" in d.current_url
        )        

    def remove_product_by_name(self, product_name):
        products = self.find_all(self.PRODUCTS)

        for product in products:
            name = product.find_element(By.CLASS_NAME, "inventory_item_name").text

            if product_name in name:
                product.find_element(By.CLASS_NAME, "btn_inventory").click()
                return

        raise Exception(f"Product '{product_name}' not found")

    def get_cart_count(self):
        try:
            text = self.get_text(self.CART_BADGE)
            return int(text)
        except:
            return 0
    
    def get_prices(self):
        elements = self.driver.find_elements(By.CLASS_NAME, "inventory_item_price")
        prices = []

        for el in elements:
            price = el.text.replace("$", "")
            prices.append(float(price))

        return prices
    
    def sort_by(self, value):
        dropdown = Select(self.driver.find_element(By.CLASS_NAME, "product_sort_container"))
        dropdown.select_by_value(value)

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "inventory_item"))
        )

    def get_all_products(self):
        return self.driver.find_elements(*self.PRODUCTS)    
    
    def is_loaded(self):
        return "inventory" in self.driver.current_url
        
