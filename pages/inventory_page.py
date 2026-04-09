from selenium.common import NoSuchElementException, StaleElementReferenceException
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

    def add_products(self, count: int):
        added = 0
        while added < count:
            try:
                products = self.driver.find_elements(By.CLASS_NAME, "inventory_item")
                for product in products:
                    # odśwież element w każdej iteracji
                    try:
                        name = product.find_element(By.CLASS_NAME, "inventory_item_name").text
                        button = product.find_element(By.TAG_NAME, "button")
                    except Exception:
                        continue  # element zniknął, spróbujemy w kolejnej iteracji

                    if button.text.lower() in ("remove", "added"):
                        continue  # pomijamy już dodane

                    button.click()
                    added += 1

                    # czekamy na badge
                    try:
                        WebDriverWait(self.driver, 10).until(
                            lambda d: (
                                (badge := d.find_elements(By.CLASS_NAME, "shopping_cart_badge"))
                                and int(badge[0].text) >= added
                            )
                        )
                    except TimeoutException:
                        print(f"[WARN] Timeout badge po dodaniu {added} produktów, spróbujemy dalej")
                    if added >= count:
                        break
            except StaleElementReferenceException:
                continue  # jeśli cała lista się przeterminowała, odświeżymy w kolejnej iteracji

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
    
    def wait_for_cart_count(self, count, timeout=15):
        """Czeka aż licznik koszyka pokaże expected count."""
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: self.get_cart_badge_count() == count
            )
        except:
            print(f"[WARN] Timeout badge po dodaniu {count} produktów, spróbujemy dalej")
            # można spróbować odświeżyć element i ponownie sprawdzić
            WebDriverWait(self.driver, timeout).until(
                lambda d: self.get_cart_badge_count() == count
            )

    def get_cart_badge_count(self):
        try:
            badge = self.driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
            return int(badge.text)
        except:
            return 0
        
