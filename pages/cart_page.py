from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CartPage(BasePage):
    CART_ITEMS = (By.CLASS_NAME, "cart_item")
    CHECKOUT_BTN = (By.ID, "checkout")
    CART_CONTAINER = (By.ID, "cart_contents_container")  # kontener koszyka
    STEP_ONE_CONTAINER = (By.ID, "checkout_info_container")

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
        self.wait_for_cart_loaded()

        checkout_btn = WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located(self.CHECKOUT_BTN)
        )

        # 🔥 force scroll to center (better than default)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", checkout_btn
        )

        # 🔥 wait a tiny moment (VERY important in CI)
        import time
        #everything failed there is must have to use time.sleep()
        time.sleep(0.5)

        # 🔥 HARD click via JS ONLY (skip selenium click completely)
        self.driver.execute_script("arguments[0].click();", checkout_btn)

        # 🔥 wait for navigation (URL FIRST)
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
        
    

    
    
    