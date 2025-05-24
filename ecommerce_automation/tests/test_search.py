# Test for Product Search

import allure
from pages.login_page import LoginPage
from pages.search_page import SearchPage
from utils.helpers import get_test_user, get_product_name

def test_search_product(driver):
    """Test searching for a product after login."""
    driver.get("https://demowebshop.tricentis.com/login")
    user = get_test_user()
    LoginPage(driver).login(user["username"], user["password"])
    driver.get("https://demowebshop.tricentis.com/")
    SearchPage(driver).search_product(get_product_name())
    assert get_product_name().lower() in driver.page_source.lower()
