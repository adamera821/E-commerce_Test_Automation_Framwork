# Test for Checkout

import allure
from pages.login_page import LoginPage
from pages.search_page import SearchPage
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from utils.helpers import get_test_user, get_product_name, get_test_address

def test_checkout(driver):
    """Test the checkout process after adding a product to the cart."""
    driver.get("https://your-ecommerce-site.com/login")
    user = get_test_user()
    LoginPage(driver).login(user["username"], user["password"])
    SearchPage(driver).search_product(get_product_name())
    ProductPage(driver).add_to_cart()
    CartPage(driver).proceed_to_checkout()
    CheckoutPage(driver).fill_details_and_place_order(get_test_address(), "creditCard")
    assert "Order Confirmation" in driver.page_source or "Thank you" in driver.page_source
