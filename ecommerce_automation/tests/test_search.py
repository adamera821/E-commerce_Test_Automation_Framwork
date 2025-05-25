# Test for Product Search

import allure
import pytest
import time
import uuid
from pages.login_page import LoginPage
from pages.search_page import SearchPage
from utils.helpers import get_test_user, get_product_name
from utils.test_logger import logger

@pytest.mark.search
@allure.feature('Product Search')
@allure.story('Search Product')
@allure.severity(allure.severity_level.CRITICAL)
def test_search_product(driver):
    """Test product search functionality."""
    test_id = str(uuid.uuid4())
    start_time = time.time()
    product_name = get_product_name()
    
    try:
        # Log test start
        logger.log_test_start(
            "test_search_product",
            browser=driver.capabilities.get('browserName', 'unknown'),
            test_id=test_id,
            environment=getattr(driver, 'test_env', 'test')
        )

        # Step 1: Navigate to search page
        logger.log_test_step("Navigate to home", "started", test_id=test_id)
        driver.get("https://demowebshop.tricentis.com/login")
        logger.log_test_step("Navigate to home", "completed", test_id=test_id)

        # Step 2: Perform product search
        logger.log_test_step("Search product", "started", 
                            test_id=test_id,
                            details={"product": product_name})
        user = get_test_user()
        LoginPage(driver).login(user["username"], user["password"])
        driver.get("https://demowebshop.tricentis.com/")
        SearchPage(driver).search_product(product_name)
        logger.log_test_step("Search product", "completed", test_id=test_id)

        # Step 3: Verify search results
        logger.log_test_step("Verify search results", "started", test_id=test_id)
        search_successful = product_name.lower() in driver.page_source.lower()
        if not search_successful:
            logger.log_test_step("Verify search results", "failed", 
                               test_id=test_id,
                               details={"search_term": product_name})
            raise AssertionError("Product search verification failed")
        logger.log_test_step("Verify search results", "completed", test_id=test_id)

        # Log successful test completion
        duration = time.time() - start_time
        logger.log_test_end(
            "test_search_product",
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
            "test_search_product",
            duration=duration,
            status="failed",
            test_id=test_id,
            details={
                "error": str(e),
                "product": product_name,
                "duration": f"{duration:.2f}s"
            }
        )
        raise

    # Add final assertion
    assert search_successful, "Product search verification failed"
