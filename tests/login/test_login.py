import time
import allure
from pages.login_page import LoginPage
import pytest
from utils.data import USER, PASSWORD, INVALID_USERS, LOCKED_USER, PERFORMANCE_USER, PROBLEM_USERS

class TestLogin:

    @allure.title("Login with valid credentials")
    @pytest.mark.smoke
    def test_login_valid(self,driver):
        login = LoginPage(driver)
        login.open()
        login.login(USER,PASSWORD)

        assert login.is_logged_in()


    
    @pytest.mark.parametrize("username,password,error", INVALID_USERS)
    def test_login_invalid(self,driver,username,password,error):
        login = LoginPage(driver)
        login.open()
        login.login(username,password)

        assert error in login.get_error()
    
    @pytest.mark.regression
    def test_login_long_username(self,driver):
        login = LoginPage(driver)
        long_user = "a" *100
        login.open()
        login.login("long_user",PASSWORD)

        assert "Username and password" in login.get_error()
    
    @pytest.mark.regression
    def test_login_locked_user(self,driver):
        login = LoginPage(driver)
        login.open()
        login.login(LOCKED_USER,PASSWORD)
        
        assert "locked out" in login.get_error()
    
    @pytest.mark.parametrize("user", PROBLEM_USERS)
    @pytest.mark.flaky
    def test_login_problem_users(self,driver,user):
        login = LoginPage(driver)
        login.open()
        login.login(user,PASSWORD)

        if user == "problem_user":
            assert login.is_logged_in()
        elif user == "error_user":
            assert login.is_logged_in()
        elif user == "visual_user":
            assert login.is_logged_in()
    
    @pytest.mark.flaky       
    def test_login_performance_user(self,driver):
        login = LoginPage(driver)
        start = time.time()

        login.open()
        login.login(PERFORMANCE_USER, PASSWORD)

        end = time.time()

        assert end - start < 10

        
