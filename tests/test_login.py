from pages.login_page import LoginPage


def test_login_invalid(driver):
    page = LoginPage(driver)
    page.open()
    page.login("standard_user", "wrong")

    assert "Username and password" in page.get_error()