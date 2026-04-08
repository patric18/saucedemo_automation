from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from utils.data import USER, PASSWORD, VALID_CHECKOUT
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

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

    # Stabilne czekanie na załadowanie koszyka w CI/CD
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.ID, "cart_contents_container"))
    )
    assert cart.is_loaded(), "CartPage did not load properly after going to cart"

    cart.go_to_checkout()
    
    assert checkout.is_step_one_loaded()

    checkout.fill_form(*VALID_CHECKOUT)
    checkout.continue_checkout()

    assert checkout.is_step_two_loaded()

    checkout.finish()

    assert "Thank you for your order!" in checkout.get_success_message()