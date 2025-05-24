# Test for Add to Cart

import allure
from pages.login_page import LoginPage
from pages.search_page import SearchPage
from pages.product_page import ProductPage
from utils.helpers import get_test_user, get_product_name

def test_add_product_to_cart(driver):
    """Test adding a searched product to the cart."""
    driver.get("https://your-ecommerce-site.com/login")
    user = get_test_user()
    LoginPage(driver).login(user["username"], user["password"])
    SearchPage(driver).search_product(get_product_name())
    ProductPage(driver).add_to_cart()
    assert "Cart" in driver.title or "added to cart" in driver.page_source.lower()
