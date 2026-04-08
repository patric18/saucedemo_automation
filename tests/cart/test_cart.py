from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from utils.data import USER, PASSWORD

def test_add_to_cart(driver):
    login = LoginPage(driver)
    inventory = InventoryPage(driver)
    cart = CartPage(driver)

    login.open()
    login.login(USER,PASSWORD)

    inventory.add_products(2)
    inventory.go_to_cart()

    assert cart.get_items_count() == 2

def test_remove_from_empty_cart(driver):
        login = LoginPage(driver)
        inventory = InventoryPage(driver)
        cart = CartPage(driver)
        
        login.open()
        login.login(USER,PASSWORD)

        assert cart.is_cart_empty()

        inventory.go_to_cart()

        cart.remove_all_products()

        assert cart.is_cart_empty()