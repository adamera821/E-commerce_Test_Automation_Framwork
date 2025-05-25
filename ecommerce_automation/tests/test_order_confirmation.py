# Test for Order Confirmation

import allure
import pytest
import time
import uuid
from pages.login_page import LoginPage
from pages.search_page import SearchPage
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from utils.helpers import get_test_user, get_product_name, get_test_address
from utils.test_logger import logger

@pytest.mark.order
@allure.feature('Order Processing')
@allure.story('Order Confirmation')
@allure.severity(allure.severity_level.CRITICAL)
def test_order_confirmation(driver):
    """Test order confirmation page after successful checkout."""
    test_id = str(uuid.uuid4())
    start_time = time.time()
    product_name = get_product_name()
    user = get_test_user()
    address = get_test_address()
    
    try:
        # Log test start
        logger.log_test_start(
            "test_order_confirmation",
            browser=driver.capabilities.get('browserName', 'unknown'),
            test_id=test_id,
            environment=getattr(driver, 'test_env', 'test')
        )

        # Step 1: Navigate to login page
        logger.log_test_step("Navigate to login page", "started", test_id=test_id)
        driver.get("https://your-ecommerce-site.com/login")
        logger.log_test_step("Navigate to login page", "completed", test_id=test_id)

        # Step 2: Login
        logger.log_test_step("Login", "started", 
                            test_id=test_id,
                            details={"username": user["username"]})
        LoginPage(driver).login(user["username"], user["password"])
        logger.log_test_step("Login", "completed", test_id=test_id)

        # Step 3: Search for product
        logger.log_test_step("Search product", "started", 
                            test_id=test_id,
                            details={"product": product_name})
        SearchPage(driver).search_product(product_name)
        logger.log_test_step("Search product", "completed", test_id=test_id)

        # Step 4: Add to cart
        logger.log_test_step("Add to cart", "started", test_id=test_id)
        ProductPage(driver).add_to_cart()
        logger.log_test_step("Add to cart", "completed", test_id=test_id)

        # Step 5: Proceed to checkout
        logger.log_test_step("Proceed to checkout", "started", test_id=test_id)
        CartPage(driver).proceed_to_checkout()
        logger.log_test_step("Proceed to checkout", "completed", test_id=test_id)

        # Step 6: Complete checkout
        logger.log_test_step("Complete checkout", "started", 
                            test_id=test_id,
                            details={"payment_method": "creditCard"})
        CheckoutPage(driver).fill_details_and_place_order(address, "creditCard")
        logger.log_test_step("Complete checkout", "completed", test_id=test_id)

        # Step 7: Verify order confirmation
        logger.log_test_step("Verify order confirmation", "started", test_id=test_id)
        assert "Order ID" in driver.page_source or "Your order has been placed" in driver.page_source
        logger.log_test_step("Verify order confirmation", "completed", test_id=test_id)

        # Log test completion
        duration = time.time() - start_time
        logger.log_test_end("test_order_confirmation", duration, "passed", test_id=test_id)

    except Exception as e:
        duration = time.time() - start_time
        logger.log_test_end("test_order_confirmation", duration, "failed", 
                           test_id=test_id,
                           error=str(e))
        raise
