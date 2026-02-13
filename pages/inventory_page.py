from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import config

from pages.base_page import BasePage


class InventoryPage(BasePage):
    TITLE = (By.CLASS_NAME, "title")
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")

    def wait_for_loaded(self, timeout=None):
        wait_time = timeout or config.EXPLICIT_WAIT
        WebDriverWait(self.driver, wait_time).until(
            EC.visibility_of_element_located(self.TITLE)
        )
        return self

    def is_loaded(self):
        return self.text_of(self.TITLE) == "Products"

    def add_item(self, item_id):
        add_button = (By.ID, f"add-to-cart-{item_id}")
        remove_button = (By.ID, f"remove-{item_id}")
        self.click(add_button)
        # Wait until the item is confirmed added before moving on.
        self.wait.until(EC.presence_of_element_located(remove_button))

    def open_cart(self):
        self.click(self.CART_LINK)
        from pages.cart_page import CartPage

        cart = CartPage(self.driver)
        try:
            cart.wait_for_loaded(timeout=5)
        except TimeoutException:
            self.driver.execute_script(
                "arguments[0].click();", self.find(self.CART_LINK)
            )
            cart.wait_for_loaded()
        return cart
