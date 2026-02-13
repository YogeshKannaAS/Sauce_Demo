from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import config
from pages.base_page import BasePage


class CheckoutPage(BasePage):
    STEP_TWO_FRAGMENT = "checkout-step-two"
    FIRST_NAME = (By.ID, "first-name")
    LAST_NAME = (By.ID, "last-name")
    POSTAL_CODE = (By.ID, "postal-code")
    CONTINUE = (By.ID, "continue")
    FINISH = (By.ID, "finish")
    COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")

    def wait_for_loaded(self, timeout=None):
        wait_time = timeout or config.EXPLICIT_WAIT
        WebDriverWait(self.driver, wait_time).until(
            EC.visibility_of_element_located(self.FIRST_NAME)
        )
        return self

    def wait_for_overview(self, timeout=None):
        wait_time = timeout or config.PAGE_LOAD_TIMEOUT

        def _is_overview(driver):
            return bool(driver.find_elements(*self.FINISH)) or (
                self.STEP_TWO_FRAGMENT in driver.current_url
            )

        WebDriverWait(self.driver, wait_time).until(_is_overview)
        return self

    def fill_info(self, first_name, last_name, postal_code):
        self.type(self.FIRST_NAME, first_name)
        self.type(self.LAST_NAME, last_name)
        self.type(self.POSTAL_CODE, postal_code)
        self.click(self.CONTINUE)
        try:
            # Fast path for normal navigation.
            self.wait_for_overview(timeout=5)
        except TimeoutException:
            # If the first click didn't navigate, try a JS click and wait again.
            self.driver.execute_script(
                "arguments[0].click();", self.find(self.CONTINUE)
            )
            self.wait_for_overview()

    def finish(self):
        self.wait_for_overview()
        self.click(self.FINISH)

    def is_complete(self):
        return self.text_of(self.COMPLETE_HEADER) == "Thank you for your order!"
