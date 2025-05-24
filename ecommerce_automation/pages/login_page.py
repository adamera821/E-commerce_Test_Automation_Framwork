# Page Object for Login Page
from selenium.webdriver.common.by import By

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.email_input = (By.ID, "Email")
        self.password_input = (By.ID, "Password")
        self.login_button = (By.CSS_SELECTOR, "input.button-1.login-button")

    def login(self, username, password):
        self.driver.find_element(*self.email_input).clear()
        self.driver.find_element(*self.email_input).send_keys(username)
        self.driver.find_element(*self.password_input).clear()
        self.driver.find_element(*self.password_input).send_keys(password)
        self.driver.find_element(*self.login_button).click()
