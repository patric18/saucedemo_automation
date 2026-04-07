from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from utils.data import USER, PASSWORD


def test_e2e_flow(driver):
    login = LoginPage(driver)
    inventory = InventoryPage(driver)

    login.open()
    login.login(USER, PASSWORD)

    inventory.add_products(2)
    assert inventory.get_cart_count() == "2"

    inventory.remove_product_by_name("Backpack")