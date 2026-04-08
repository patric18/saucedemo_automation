from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from utils.data import USER, PASSWORD, INVALID_CHECKOUT, VALID_CHECKOUT
import pytest

def test_checkout_success(driver):
    login = LoginPage(driver)
    inventory = InventoryPage(driver)
    cart = CartPage(driver)
    checkout = CheckoutPage(driver)

    login.open()
    login.login(USER,PASSWORD)

    inventory.add_products(1)
    inventory.go_to_cart()
    cart.go_to_checkout()

    checkout.fill_form(*VALID_CHECKOUT)
    checkout.continue_checkout()
    checkout.finish()

    assert "THANK YOU" in checkout.get_success_message().upper()

@pytest.mark.parametrize("firstname,lastname,postalcode,error", INVALID_CHECKOUT)
def test_checkout_missing_data(driver,firstname,lastname,postalcode,error):
    login = LoginPage(driver)
    inventory = InventoryPage(driver)
    cart = CartPage(driver)
    checkout = CheckoutPage(driver)   

    login.open()
    login.login(USER,PASSWORD)

    inventory.add_products(1)
    inventory.go_to_cart()
    cart.go_to_checkout()

    checkout.fill_form(firstname,lastname,postalcode)
    checkout.continue_checkout(wait_for_step_two=False)

    assert checkout.get_error_message() == error

    #error_message = checkout.get_error()
    #assert error in error_message, f"Expected error '{error}' but got '{error_message}'"
