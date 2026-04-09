from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from utils.data import USER, PASSWORD, INVALID_CHECKOUT, VALID_CHECKOUT
import pytest
import time

def test_checkout_success(driver):
    login = LoginPage(driver)
    inventory = InventoryPage(driver)
    cart = CartPage(driver)
    checkout = CheckoutPage(driver)

    login.open()
    login.login(USER, PASSWORD)

    inventory.add_products(1)
    inventory.go_to_cart()
    cart.go_to_checkout()

    checkout.fill_form(*VALID_CHECKOUT)
    time.sleep(0.3)  # krótka pauza dla JS
    print("Checkout form values:", *VALID_CHECKOUT)
    
    checkout.continue_checkout()
    checkout.finish()

    assert "THANK YOU" in checkout.get_success_message().upper()


@pytest.mark.parametrize("firstname,lastname,postalcode,error", INVALID_CHECKOUT)
def test_checkout_missing_data(driver, firstname, lastname, postalcode, error):
    login = LoginPage(driver)
    inventory = InventoryPage(driver)
    cart = CartPage(driver)
    checkout = CheckoutPage(driver)   

    login.open()
    login.login(USER, PASSWORD)

    inventory.add_products(1)
    inventory.go_to_cart()
    cart.go_to_checkout()

    checkout.fill_form(*INVALID_CHECKOUT)
    time.sleep(0.3)  # krótka pauza dla JS
    checkout.continue_checkout(wait_for_step_two=False)

    actual_error = checkout.get_error_message()
    print(f"Expected error: '{error}' | Actual error: '{actual_error}'")
    assert actual_error == error