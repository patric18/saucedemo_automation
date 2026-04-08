from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from utils.data import USER, PASSWORD
from selenium.webdriver.common.by import By


def test_inventory_items_have_full_data(driver):
    login = LoginPage(driver)
    inventory = InventoryPage(driver)
    cart = CartPage(driver)

    

    login.open()
    login.login(USER,PASSWORD)

    products = inventory.get_all_products()

    for product in products:
        name = product.find_element(By.CLASS_NAME, "inventory_item_name")
        price = product.find_element(By.CLASS_NAME, "inventory_item_price")
        img = product.find_element(By.TAG_NAME, "img")

        assert name.text != ""
        assert price.text.startswith("$")
        assert img.get_attribute("src") != ""

def test_sorting(driver):
    login = LoginPage(driver)
    inventory = InventoryPage(driver)

    login.open()
    login.login(USER,PASSWORD)

    inventory.sort_by("lohi")

    prices = inventory.get_prices()
    
    assert prices == sorted(prices)        