from selenium.webdriver.common.by import By

import config
from pages.base_page import BasePage


class LoginPage(BasePage):
    USERNAME = (By.ID, "user-name")
    PASSWORD = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR = (By.CSS_SELECTOR, "h3[data-test='error']")

    def load(self):
        self.open(config.BASE_URL)

    def login_as(self, username, password):
        self.type(self.USERNAME, username)
        self.type(self.PASSWORD, password)
        self.click(self.LOGIN_BUTTON)
        from pages.inventory_page import InventoryPage

        return InventoryPage(self.driver)

    def error_message(self):
        return self.text_of(self.ERROR)
