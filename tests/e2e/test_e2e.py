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
    cart = CartPage(driver)
    checkout = CheckoutPage(driver)

    login.open()
    login.login(USER, PASSWORD)
    assert inventory.is_loaded()

    inventory.add_products(1)
    assert inventory.get_cart_count() == "1"

    inventory.go_to_cart()

    # Czekamy na obecność koszyka
    WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located((By.ID, "cart_contents_container"))
    )
    assert cart.is_loaded()

    cart.go_to_checkout()

    # Czekamy na checkout-step-one w DOM + URL
    WebDriverWait(driver, 30).until(lambda d: "checkout-step-one" in d.current_url)
    WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located((By.ID, "checkout-info-container"))
    )
    assert checkout.is_step_one_loaded()

    checkout.fill_form(*VALID_CHECKOUT)
    checkout.continue_checkout()

    assert checkout.is_step_two_loaded()

    checkout.finish()

    assert "Thank you for your order!" in checkout.get_success_message()