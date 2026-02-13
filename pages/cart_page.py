from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import config

from pages.base_page import BasePage


class CartPage(BasePage):
    CART_LIST = (By.CLASS_NAME, "cart_list")
    CHECKOUT = (By.ID, "checkout")
    CONTINUE_SHOPPING = (By.ID, "continue-shopping")
    ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")

    def wait_for_loaded(self, timeout=None):
        wait_time = timeout or config.EXPLICIT_WAIT
        WebDriverWait(self.driver, wait_time).until(
            EC.visibility_of_element_located(self.CART_LIST)
        )
        return self

    def has_item_named(self, name):
        self.wait_for_loaded()

        def _has_item(_driver):
            names = [el.text for el in _driver.find_elements(*self.ITEM_NAME)]
            return name in names

        try:
            return self.wait.until(_has_item)
        except TimeoutException:
            return False

    def checkout(self):
        self.click(self.CHECKOUT)
        from pages.checkout_page import CheckoutPage

        checkout = CheckoutPage(self.driver)
        try:
            checkout.wait_for_loaded(timeout=5)
        except TimeoutException:
            self.driver.execute_script(
                "arguments[0].click();", self.find(self.CHECKOUT)
            )
            checkout.wait_for_loaded()
        return checkout

    def continue_shopping(self):
        self.click(self.CONTINUE_SHOPPING)
        from pages.inventory_page import InventoryPage

        inventory = InventoryPage(self.driver)
        try:
            inventory.wait_for_loaded(timeout=5)
        except TimeoutException:
            self.driver.execute_script(
                "arguments[0].click();", self.find(self.CONTINUE_SHOPPING)
            )
            inventory.wait_for_loaded()
        return inventory
