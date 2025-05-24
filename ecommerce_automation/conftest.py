# Pytest fixtures and configuration

import pytest
from selenium import webdriver

@pytest.fixture(scope="function")
def driver(request):
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    # Get the result of the test
    outcome = yield
    rep = outcome.get_result()
    # Only take screenshot for actual test calls, not setup/teardown
    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get("driver")
        if driver:
            screenshot_path = f"allure-results/{item.name}.png"
            driver.save_screenshot(screenshot_path)
            try:
                import allure
                from allure_commons.types import AttachmentType
                allure.attach.file(screenshot_path, name="screenshot", attachment_type=AttachmentType.PNG)
            except ImportError:
                pass
