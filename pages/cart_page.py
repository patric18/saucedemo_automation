from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CartPage(BasePage):
    CART_ITEMS = (By.CLASS_NAME, "cart_item")
    CHECKOUT_BTN = (By.ID, "checkout")
    CART_CONTAINER = (By.ID, "cart_contents_container")  # kontener koszyka

    def wait_for_cart_loaded(self, timeout=10):
        WebDriverWait(self.driver, timeout).until(
            lambda d: "/cart.html" in d.current_url
        )
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
        self.wait_for_cart_loaded()
        return len(self.driver.find_elements(*self.CART_ITEMS))

    def go_to_checkout(self):
        # 1. Wait for cart page to load
        self.wait_for_cart_loaded()

        # 2. Wait for checkout button to be clickable
        checkout_btn = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable(self.CHECKOUT_BTN)
        )

        # 3. Click checkout
        checkout_btn.click()

        # 4. Wait until step one page is loaded
        WebDriverWait(self.driver, 15).until(
            lambda d: "checkout-step-one" in d.current_url
        )

    def is_cart_empty(self):
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
        try:
            self.wait_for_cart_loaded()
            return True
        except:
            print("CartPage did not load:", self.driver.current_url)
            return False
        
    STEP_ONE_CONTAINER = (By.ID, "checkout_info_container")

    def is_step_one_loaded(self):
        try:
            WebDriverWait(self.driver, 10).until(
                lambda d: "checkout-step-one" in d.current_url
            )
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.STEP_ONE_CONTAINER)
            )
            return True
        except:
            print("FAILED STEP ONE, URL:", self.driver.current_url)
            return False
    
    