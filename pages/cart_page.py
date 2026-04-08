from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CartPage(BasePage):
    CART_ITEMS = (By.CLASS_NAME, "cart_item")
    CHECKOUT_BTN = (By.ID, "checkout")
    CART_CONTAINER = (By.ID, "cart_contents_container")  # kontener koszyka

    def wait_for_cart_loaded(self, timeout=20):
        """Czeka, aż kontener koszyka będzie widoczny."""
        WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(self.CART_CONTAINER)
        )

    def wait_for_page_loaded(self, timeout=20):
        """Czeka aż URL będzie '/cart.html' i kontener koszyka będzie widoczny."""
        WebDriverWait(self.driver, timeout).until(
            lambda d: "/cart.html" in d.current_url
        )
        self.wait_for_cart_loaded(timeout=timeout)

    def get_items_count(self):
        """Zwraca liczbę produktów w koszyku."""
        self.wait_for_cart_loaded()
        return len(self.driver.find_elements(*self.CART_ITEMS))

    def go_to_checkout(self):
        """Przejście do strony checkout."""
        self.wait_for_cart_loaded()
        self.click(self.CHECKOUT_BTN)

    def is_cart_empty(self):
        """Sprawdza, czy koszyk jest pusty (True/False)."""
        self.wait_for_cart_loaded()
        return len(self.driver.find_elements(*self.CART_ITEMS)) == 0

    def remove_all_products(self):
        """Usuwa wszystkie produkty z koszyka, dynamicznie pobierając przyciski."""
        self.wait_for_cart_loaded()
        while True:
            buttons = self.driver.find_elements(By.XPATH, "//button[text()='Remove']")
            if not buttons:
                break
            for btn in buttons:
                btn.click()

    def is_loaded(self):
        """Sprawdza, czy strona koszyka jest w pełni załadowana."""
        try:
            self.wait_for_page_loaded()
            return True
        except Exception as e:
            print("CartPage did not load:", e)
            return False