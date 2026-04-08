from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from utils.data import USER, PASSWORD, VALID_CHECKOUT
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def test_e2e_flow(driver):
    login = LoginPage(driver)
    inventory = InventoryPage(driver)
    cart = CartPage(driver)
    checkout = CheckoutPage(driver)

    # Login
    login.open()
    login.login(USER, PASSWORD)
    assert inventory.is_loaded()

    # Dodaj produkt
    inventory.add_products(1)
    assert inventory.get_cart_count() == "1"

    # Przejdź do koszyka
    inventory.go_to_cart()

    # Czekamy na obecność koszyka w DOM
    WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located((By.ID, "cart_contents_container"))
    )
    assert cart.is_loaded()

    # Przejdź do checkout
    cart.go_to_checkout()

    # Czekamy **tylko na kontener Step One** w DOM
    WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located((By.ID, "checkout-info-container"))
    )
    assert checkout.is_step_one_loaded()

    # Wypełnij formularz i kontynuuj
    checkout.fill_form(*VALID_CHECKOUT)
    checkout.continue_checkout()

    # Czekamy **tylko na kontener Step Two** w DOM
    WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located((By.ID, "checkout_summary_container"))
    )
    assert checkout.is_step_two_loaded()

    # Zakończ i sprawdź komunikat
    checkout.finish()
    WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "complete-header"))
    )
    assert "Thank you for your order!" in checkout.get_success_message()