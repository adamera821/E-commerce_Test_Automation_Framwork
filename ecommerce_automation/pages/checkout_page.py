# Page Object for Checkout Page
from selenium.webdriver.common.by import By

class CheckoutPage:
    def __init__(self, driver):
        self.driver = driver
        self.address_input = (By.ID, "address")
        self.payment_method_radio = (By.ID, "creditCard")  # Example: creditCard
        self.place_order_button = (By.ID, "placeOrderBtn")

    def fill_details_and_place_order(self, address, payment_method_id="creditCard"):
        self.driver.find_element(*self.address_input).send_keys(address)
        self.driver.find_element(By.ID, payment_method_id).click()
        self.driver.find_element(*self.place_order_button).click()
