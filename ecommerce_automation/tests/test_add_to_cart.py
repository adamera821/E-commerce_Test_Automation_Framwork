# Test for Add to Cart

import allure
import pytest
import time
import uuid
from pages.login_page import LoginPage
from pages.search_page import SearchPage
from pages.product_page import ProductPage
from utils.helpers import get_test_user, get_product_name
from utils.test_logger import logger

@pytest.mark.cart
@allure.feature('Shopping Cart')
@allure.story('Add to Cart')
@allure.severity(allure.severity_level.CRITICAL)
def test_add_product_to_cart(driver):
    """Test adding a searched product to the cart."""
    test_id = str(uuid.uuid4())
    start_time = time.time()
    product_name = get_product_name()
    user = get_test_user()
    
    try:
        # Log test start
        logger.log_test_start(
            "test_add_product_to_cart",
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

        # Step 5: Verify cart
        logger.log_test_step("Verify cart", "started", test_id=test_id)
        cart_verified = "Cart" in driver.title or "added to cart" in driver.page_source.lower()
        if not cart_verified:
            logger.log_test_step("Verify cart", "failed", 
                               test_id=test_id,
                               details={"page_title": driver.title})
            raise AssertionError("Cart verification failed")
        logger.log_test_step("Verify cart", "completed", test_id=test_id)

        # Log successful test completion
        duration = time.time() - start_time
        logger.log_test_end(
            "test_add_product_to_cart",
            duration=duration,
            status="passed",
            test_id=test_id,
            details={
                "product": product_name,
                "duration": f"{duration:.2f}s"
            }
        )

    except Exception as e:
        # Log test failure
        duration = time.time() - start_time
        logger.log_test_end(
            "test_add_product_to_cart",
            duration=duration,
            status="failed",
            test_id=test_id,
            details={
                "error": str(e),
                "product": product_name,
                "duration": f"{duration:.2f}s"
            }
        )
        # Re-raise the exception for pytest to handle
        raise

    # Add final assertion
    assert cart_verified, "Product was not successfully added to cart"
