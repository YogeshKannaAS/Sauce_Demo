from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import config


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, config.EXPLICIT_WAIT)

    def open(self, url):
        self.driver.get(url)

    def find(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def click(self, locator):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        # Ensure offscreen elements are brought into view before clicking.
        try:
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center', inline: 'center'});",
                element,
            )
        except Exception:
            pass
        element.click()

    def type(self, locator, value):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        if value is None:
            return
        current_value = ""
        try:
            current_value = element.get_attribute("value") or ""
        except Exception:
            current_value = ""
        if value == "":
            if current_value:
                element.clear()
            if element.get_attribute("value") != "":
                self.driver.execute_script(
                    "arguments[0].value = '';"
                    "arguments[0].dispatchEvent(new Event('input', {bubbles: true}));"
                    "arguments[0].dispatchEvent(new Event('change', {bubbles: true}));",
                    element,
                )
            return
        if current_value and current_value != value:
            element.clear()
        if current_value != value:
            element.send_keys(value)
        if (element.get_attribute("value") or "") != value:
            # Fallback to JS set + input/change events if send_keys didn't stick.
            self.driver.execute_script(
                "arguments[0].value = arguments[1];"
                "arguments[0].dispatchEvent(new Event('input', {bubbles: true}));"
                "arguments[0].dispatchEvent(new Event('change', {bubbles: true}));",
                element,
                value,
            )

    def text_of(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator)).text

    def is_visible(self, locator):
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False
