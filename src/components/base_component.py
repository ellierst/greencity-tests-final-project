from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure

class BaseComponent:
    def __init__(self, driver, locator=None, wait_time=10):
        self.driver = driver
        self.locator = locator
        self.wait = WebDriverWait(driver, wait_time)

    @property
    @allure.step("Get element")
    def element(self):
        if self.locator is None:
            raise ValueError("Locator not set for this component")
        return self.wait.until(EC.presence_of_element_located(self.locator))

    @allure.step("Check if base component is displayed")
    def is_displayed(self):
        try:
            return self.element.is_displayed()
        except Exception:
            return False

    @allure.step("Check if base component is enabled")
    def is_enabled(self):
        try:
            return self.element.is_enabled()
        except Exception:
            return False

    @allure.step("Click on base component")
    def click(self):
        element = self.wait.until(EC.element_to_be_clickable(self.locator))
        element.click()

    @allure.step("Get text {by} {value}")
    def find_element(self, by, value):
        return self.element.find_element(by, value)

    @allure.step("Find all elements matching the given criteria: {by}, {value}")
    def find_elements(self, by, value):
        return self.element.find_elements(by, value)

    @allure.step("Get attribute {attribute}")
    def get_attribute(self, attribute):
        return self.element.get_attribute(attribute)

    @allure.step("Send keys")
    def send_keys(self, text):
        element = self.wait.until(EC.visibility_of_element_located(self.locator))
        element.send_keys(text)

    @allure.step("Clear text")
    def clear(self):
        element = self.wait.until(EC.visibility_of_element_located(self.locator))
        element.clear()
