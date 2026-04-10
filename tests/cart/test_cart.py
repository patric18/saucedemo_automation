from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from utils.data import USER, PASSWORD
import pytest

@pytest.mark.smoke
def test_add_to_cart(driver):
    login = LoginPage(driver)
    inventory = InventoryPage(driver)
    cart = CartPage(driver)

    login.open()
    login.login(USER,PASSWORD)
    inventory.wait_until_loaded()


    inventory.add_products(1)
    inventory.wait_for_cart_count(1)
    inventory.go_to_cart()

    assert cart.get_items_count() == 1

@pytest.mark.regression
def test_remove_from_empty_cart(driver):
        login = LoginPage(driver)
        inventory = InventoryPage(driver)
        cart = CartPage(driver)
        
        login.open()
        login.login(USER,PASSWORD)

        inventory.go_to_cart()

        assert cart.is_cart_empty()

        cart.remove_all_products()

        assert cart.is_cart_empty()

@pytest.mark.smoke
def test_cart_page_loads(driver):
    login = LoginPage(driver)
    inventory = InventoryPage(driver)

    login.open()
    login.login(USER, PASSWORD)

    assert inventory.is_loaded()