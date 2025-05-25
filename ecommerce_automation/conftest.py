# Pytest fixtures and configuration

import pytest
from selenium import webdriver
from datetime import datetime
from utils.db_manager import TestResultsDB

# Initialize DB
test_db = TestResultsDB()
current_run_id = None

def pytest_configure(config):
    """Called before test run starts"""
    global current_run_id
    current_run_id = test_db.start_test_run()

def pytest_sessionfinish(session):
    """Called after test run completes"""
    passed = session.testscollected - session.testsfailed
    test_db.end_test_run(current_run_id, session.testscollected, passed, session.testsfailed)

@pytest.fixture(scope="function")
def driver(request):
    start_time = datetime.now()
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    
    # Calculate test execution time
    execution_time = (datetime.now() - start_time).total_seconds()
    
    # Store test result in database
    if hasattr(request.node, 'rep_call'):
        status = 'passed' if request.node.rep_call.passed else 'failed'
        error_message = None
        screenshot_path = None
        
        if status == 'failed':
            screenshot_path = f"allure-results/{request.node.name}.png"
            driver.save_screenshot(screenshot_path)
            error_message = str(request.node.rep_call.longrepr)
            
            try:
                import allure
                from allure_commons.types import AttachmentType
                allure.attach.file(screenshot_path, name="screenshot", attachment_type=AttachmentType.PNG)
            except ImportError:
                pass
        
        test_db.save_test_result(
            current_run_id,
            request.node.name,
            status,
            error_message,
            screenshot_path,
            execution_time
        )
    
    driver.quit()

@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
