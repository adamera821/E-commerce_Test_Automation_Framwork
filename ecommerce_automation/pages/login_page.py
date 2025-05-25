# Page Object for Login Page
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.email_input = (By.CSS_SELECTOR, 'input[type="email"], input[name="email"], #email, #Email')
        self.password_input = (By.CSS_SELECTOR, 'input[type="password"], input[name="password"], #password, #Password')
        self.login_button = (By.CSS_SELECTOR, 'button[type="submit"], input[type="submit"], .login-button')

    def login(self, username, password):
        email_field = self.wait.until(EC.presence_of_element_located(self.email_input))
        email_field.clear()
        email_field.send_keys(username)

        password_field = self.wait.until(EC.presence_of_element_located(self.password_input))
        password_field.clear()
        password_field.send_keys(password)

        submit_button = self.wait.until(EC.element_to_be_clickable(self.login_button))
        submit_button.click()
