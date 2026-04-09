from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.common.exceptions import TimeoutException

class InventoryPage(BasePage):

    PRODUCTS = (By.CLASS_NAME, "inventory_item")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    PRODUCT_ADD_BUTTONS = (By.CLASS_NAME, "btn_inventory")

    def add_products(self, count=1):
        products = self.driver.find_elements(By.CSS_SELECTOR, ".inventory_item")
        added = 0
        added_names = set()  # żeby nie dodać tego samego produktu dwa razy

        print(f"[DEBUG] Chcemy dodać {count} produktów. Razem na stronie: {len(products)}")

        for product in products:
            if added >= count:
                break

            name = product.find_element(By.CLASS_NAME, "inventory_item_name").text
            btn = product.find_element(By.CSS_SELECTOR, "button")
            
            if name in added_names:
                continue  # już dodane

            if btn.text.lower() == "add to cart":
                print(f"[DEBUG] Produkt: {name} | przycisk: {btn.text}")
                btn.click()
                added += 1
                added_names.add(name)
                print(f"[DEBUG] Kliknięto 'Add to cart'. Dodano {added} produktów.")

        # Czekamy aż badge pokaże liczbę dodanych produktów
        try:
            WebDriverWait(self.driver, 10).until(
                lambda d: (
                    (badge := d.find_elements(By.CLASS_NAME, "shopping_cart_badge"))
                    and int(badge[0].text) >= added
                )
            )
            print(f"[DEBUG] Koszyk odzwierciedla {added} produktów.")
        except TimeoutException as e:
            print(f"[ERROR] Timeout przy oczekiwaniu na badge koszyka! Dodano {added} produktów.")
            timestamp = int(time.time())
            self.driver.save_screenshot(f"debug_inventory_{timestamp}.png")
            raise e

    def go_to_cart(self):
        """Click the cart icon. Waits for page ready and uses JS click to avoid timeouts."""
        # Wait until the page is fully loaded
        WebDriverWait(self.driver, 10).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        # Find the cart icon
        cart_icon = self.driver.find_element(*self.CART_LINK)
        # Click using JavaScript to avoid element not clickable issues
        self.driver.execute_script("arguments[0].click();", cart_icon)

    def remove_product_by_name(self, product_name):
        products = self.find_all(self.PRODUCTS)

        for product in products:
            name = product.find_element(By.CLASS_NAME, "inventory_item_name").text

            if product_name in name:
                product.find_element(By.CLASS_NAME, "btn_inventory").click()
                return

        raise Exception(f"Product '{product_name}' not found")

    def _get_cart_count_safe(self):
        try:
            badge = self.driver.find_element(*self.CART_BADGE)
            text = badge.text.strip()
            return int(text) if text.isdigit() else 0
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
    
    def wait_for_cart_count(self, expected_count: int):
        WebDriverWait(self.driver, 10).until(
            lambda d: self._get_cart_count_safe() >= expected_count
        )

    def _get_cart_count_safe(self) -> int:
        """Return cart count, 0 if badge is missing"""
        try:
            badge = self.driver.find_element(*self.CART_BADGE)
            return int(badge.text)
        except (NoSuchElementException, ValueError):
            return 0
        
