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

    # Stabilne czekanie na kontener koszyka
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.ID, "cart_contents_container"))
    )
    assert cart.is_loaded(), "CartPage did not load properly after going to cart"

    cart.go_to_checkout()

    # NOWE: czekaj aż URL checkout-step-one będzie załadowany i kontener step 1 widoczny
    WebDriverWait(driver, 30).until(
        lambda d: "checkout-step-one" in d.current_url
    )
    WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.ID, "checkout-info-container"))
    )

    assert checkout.is_step_one_loaded(timeout=30), "Checkout Step 1 did not load in time"

    checkout.fill_form(*VALID_CHECKOUT)
    checkout.continue_checkout()

    assert checkout.is_step_two_loaded(timeout=30), "Checkout Step 2 did not load in time"

    checkout.finish()

    assert "Thank you for your order!" in checkout.get_success_message()