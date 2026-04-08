from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from utils.data import USER, PASSWORD, VALID_CHECKOUT
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def test_e2e_flow(driver):
    login = LoginPage(driver)
    inventory = InventoryPage(driver)
    assert inventory.get_cart_count() == 0
    cart = CartPage(driver)
    checkout = CheckoutPage(driver)
    

    # Login
    login.open()
    login.login(USER, PASSWORD)
    assert inventory.is_loaded()

    # Dodaj produkt
    inventory.add_products(3)
    assert inventory.get_cart_count() == 3

    # Przejdź do koszyka
    inventory.go_to_cart()
    print("URL AFTER CLICK:", driver.current_url)
    ##assert cart.get_items_count() == 3

    # Checkout
    cart.go_to_checkout()

    print("URL AFTER CLICK:", driver.current_url)

    #assert checkout.is_step_one_loaded()

    checkout.fill_form(*VALID_CHECKOUT)
    checkout.continue_checkout()
    print("URL AFTER CLICK:", driver.current_url)
    #assert checkout.is_step_two_loaded()

    checkout.finish()
    print("URL AFTER CLICK:", driver.current_url)
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "complete-header"))
    )
    assert "Thank you for your order!" in checkout.get_success_message()