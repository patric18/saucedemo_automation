from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from utils.data import USER, PASSWORD

def test_sorting(driver):
    login = LoginPage(driver)
    inventory = InventoryPage(driver)

    login.open()
    login.login(USER,PASSWORD)

    inventory.add_products(3)
    inventory.sort_by("lohi")

    prices = inventory.get_prices()
    
    assert prices == sorted(prices)
