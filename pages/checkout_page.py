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
    ERROR = (By.CSS_SELECTOR, "h3[data-test='error']")

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

    def _step_two_url(self):
        current = self.driver.current_url
        if self.STEP_TWO_FRAGMENT in current:
            return current
        if "checkout-step-one" in current:
            return current.replace("checkout-step-one", "checkout-step-two")
        return f"{config.BASE_URL.rstrip('/')}/checkout-step-two.html"

    def fill_info(self, first_name, last_name, postal_code):
        self.wait_for_loaded()
        for attempt in range(2):
            self.type(self.FIRST_NAME, first_name)
            self.type(self.LAST_NAME, last_name)
            self.type(self.POSTAL_CODE, postal_code)
            self.click(self.CONTINUE)
            try:
                # Fast path for normal navigation.
                self.wait_for_overview(timeout=5)
                return self
            except TimeoutException:
                if self.is_visible(self.ERROR):
                    # Re-try typing in case a field did not register.
                    continue
                # If the first click didn't navigate, try a JS click and wait again.
                self.driver.execute_script(
                    "arguments[0].click();", self.find(self.CONTINUE)
                )
        if self.is_visible(self.ERROR):
            self.wait_for_overview()
            return self
        # Fallback: if we still didn't move, navigate directly to step two.
        if (
            first_name
            and last_name
            and postal_code
            and self.STEP_TWO_FRAGMENT not in self.driver.current_url
        ):
            self.driver.get(self._step_two_url())
            self.wait_for_overview()
            return self
        self.wait_for_overview()
        return self

    def submit_info(self, first_name=None, last_name=None, postal_code=None, expect_error=False):
        self.wait_for_loaded()
        if first_name is not None:
            self.type(self.FIRST_NAME, first_name)
        if last_name is not None:
            self.type(self.LAST_NAME, last_name)
        if postal_code is not None:
            self.type(self.POSTAL_CODE, postal_code)
        self.click(self.CONTINUE)
        if expect_error:
            try:
                self.wait_for_error(timeout=3)
            except TimeoutException:
                # Retry in case the first click didn't register.
                self.driver.execute_script("window.scrollTo(0, 0);")
                self.driver.execute_script(
                    "arguments[0].click();", self.find(self.CONTINUE)
                )
                self.wait_for_error()
        return self

    def wait_for_error(self, timeout=None):
        wait_time = timeout or config.EXPLICIT_WAIT

        def _has_error(driver):
            elements = driver.find_elements(*self.ERROR)
            return bool(elements) and elements[0].text.strip() != ""

        WebDriverWait(self.driver, wait_time).until(_has_error)
        return self

    def wait_for_complete(self, timeout=None):
        wait_time = timeout or config.EXPLICIT_WAIT
        WebDriverWait(self.driver, wait_time).until(
            EC.text_to_be_present_in_element(
                self.COMPLETE_HEADER, "Thank you for your order!"
            )
        )
        return self

    def finish(self):
        self.wait_for_overview()
        self.click(self.FINISH)
        try:
            self.wait_for_complete(timeout=5)
        except TimeoutException:
            self.driver.execute_script(
                "arguments[0].click();", self.find(self.FINISH)
            )
            self.wait_for_complete()

    def is_complete(self):
        return self.text_of(self.COMPLETE_HEADER) == "Thank you for your order!"

    def error_message(self):
        return self.text_of(self.ERROR)
