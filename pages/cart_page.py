from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class CartPage(BasePage):
    CART_LIST = (By.CLASS_NAME, "cart_list")
    CHECKOUT = (By.ID, "checkout")
    ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")

    def has_item_named(self, name):
        self.wait.until(EC.visibility_of_element_located(self.CART_LIST))

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

        return CheckoutPage(self.driver)
