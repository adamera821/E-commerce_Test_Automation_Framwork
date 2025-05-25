# Test for Login

import allure
import pytest
import time
import uuid
from pages.login_page import LoginPage
from utils.helpers import get_test_user
from utils.test_logger import logger

@pytest.mark.auth
@allure.feature('Authentication')
@allure.story('User Login')
@allure.severity(allure.severity_level.BLOCKER)
def test_valid_login(driver):
    """Test valid login scenario with correct credentials."""
    test_id = str(uuid.uuid4())
    start_time = time.time()
    user = get_test_user()
    
    try:
        # Log test start
        logger.log_test_start(
            "test_valid_login",
            browser=driver.capabilities.get('browserName', 'unknown'),
            test_id=test_id,
            environment=getattr(driver, 'test_env', 'test')
        )

        # Step 1: Navigate to login page
        logger.log_test_step("Navigate to login page", "started", test_id=test_id)
        driver.get("https://your-ecommerce-site.com/login")
        logger.log_test_step("Navigate to login page", "completed", test_id=test_id)

        # Step 2: Perform login
        logger.log_test_step("Login", "started", 
                            test_id=test_id,
                            details={"username": user["username"]})
        LoginPage(driver).login(user["username"], user["password"])
        logger.log_test_step("Login", "completed", test_id=test_id)

        # Step 3: Verify login success
        logger.log_test_step("Verify login", "started", test_id=test_id)
        login_successful = "dashboard" in driver.current_url.lower() or "account" in driver.current_url.lower()
        if not login_successful:
            logger.log_test_step("Verify login", "failed", 
                               test_id=test_id,
                               details={"current_url": driver.current_url})
            raise AssertionError("Login verification failed")
        logger.log_test_step("Verify login", "completed", test_id=test_id)

        # Log successful test completion
        duration = time.time() - start_time
        logger.log_test_end(
            "test_valid_login",
            duration=duration,
            status="passed",
            test_id=test_id,
            details={
                "duration": f"{duration:.2f}s",
                "username": user["username"]
            }
        )

    except Exception as e:
        # Log test failure
        duration = time.time() - start_time
        logger.log_test_end(
            "test_valid_login",
            duration=duration,
            status="failed",
            test_id=test_id,
            details={
                "error": str(e),
                "duration": f"{duration:.2f}s"
            }
        )
        raise

    # Add final assertion
    assert login_successful, "Login verification failed"
