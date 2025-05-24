# Test for Login

import allure
from pages.login_page import LoginPage
from utils.helpers import get_test_user

def test_valid_login(driver):
    """Test valid login scenario with correct credentials."""
    driver.get("https://your-ecommerce-site.com/login")
    user = get_test_user()
    LoginPage(driver).login(user["username"], user["password"])
    assert "dashboard" in driver.current_url or "Welcome" in driver.page_source
