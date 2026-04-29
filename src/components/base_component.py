from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BaseComponent:
    def __init__(self, driver, locator=None, wait_time=10):
        self.driver = driver
        self.locator = locator
        self.wait = WebDriverWait(driver, wait_time)

    @property
    def element(self):
        if self.locator is None:
            raise ValueError("Locator not set for this component")
        return self.wait.until(EC.presence_of_element_located(self.locator))

    def is_displayed(self):
        try:
            return self.element.is_displayed()
        except Exception:
            return False

    def is_enabled(self):
        try:
            return self.element.is_enabled()
        except Exception:
            return False

    def click(self):
        element = self.wait.until(EC.element_to_be_clickable(self.locator))
        element.click()

    def find_element(self, by, value):
        return self.element.find_element(by, value)

    def find_elements(self, by, value):
        return self.element.find_elements(by, value)

    def get_attribute(self, attribute):
        return self.element.get_attribute(attribute)

    def send_keys(self, text):
        element = self.wait.until(EC.visibility_of_element_located(self.locator))
        element.send_keys(text)

    def clear(self):
        element = self.wait.until(EC.visibility_of_element_located(self.locator))
        element.clear()
