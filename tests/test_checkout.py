from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from utils.data import USER, PASSWORD

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

    checkout.fill_form("JAN", "Test", "00-001")
    checkout.continue_checkout()
    checkout.finish()

    assert "THANK YOU" in checkout.get_success_message().upper()

def test_checkout_missing_data(driver):
    login = LoginPage(driver)
    inventory = InventoryPage(driver)
    cart = CartPage(driver)
    checkout = CheckoutPage(driver)   

    login.open()
    login.login(USER,PASSWORD)

    inventory.add_products(1)
    inventory.go_to_cart()
    cart.go_to_checkout()

    checkout.fill_form("", "Test", "00-001")
    checkout.continue_checkout()

    assert "First Name is required" in checkout.get_error()
