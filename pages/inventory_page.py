from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class InventoryPage(BasePage):
    TITLE = (By.CLASS_NAME, "title")
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")

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

        return CartPage(self.driver)
