# Page Object for Search Page

from selenium.webdriver.common.by import By

class SearchPage:
    def __init__(self, driver):
        self.driver = driver
        self.search_box = (By.ID, "small-searchterms")
        self.search_button = (By.CSS_SELECTOR, "input.button-1.search-box-button")

    def search_product(self, product_name):
        self.driver.find_element(*self.search_box).clear()
        self.driver.find_element(*self.search_box).send_keys(product_name)
        self.driver.find_element(*self.search_button).click()
