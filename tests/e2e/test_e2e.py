from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from utils.data import USER, PASSWORD, VALID_CHECKOUT
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.mark.e2e
@pytest.mark.smoke
@pytest.mark.flaky
def test_e2e_flow(driver):
    login = LoginPage(driver)
    inventory = InventoryPage(driver)
    cart = CartPage(driver)
    checkout = CheckoutPage(driver)

    login.open()
    login.login(USER, PASSWORD)
    inventory.wait_until_loaded()
    assert inventory.is_loaded()

    inventory.add_products(1)
    inventory.wait_for_cart_count(1)
    inventory.go_to_cart()
    assert cart.get_items_count() == 1

    cart.go_to_checkout()
    checkout.wait_for_step_one()

    checkout.fill_form(*VALID_CHECKOUT)
    checkout.continue_checkout()
    checkout.wait_for_step_two()

    checkout.finish()
    assert "Thank you for your order!" in checkout.get_success_message()