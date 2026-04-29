from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    sign_in_button_locator = (By.CSS_SELECTOR, ".header_navigation-menu-right-list > .header_sign-in-link")
    sign_in_button_alt_locator = (By.XPATH, "//a[contains(text(), 'Sign in') or contains(text(), 'Увійти')]")
    events_link_locator = (By.XPATH, "//header//a[contains(@class, 'url-name') and contains(., 'Події') or contains(., 'Events')]")

    def __init__(self, driver, wait_time=30):
        self.driver = driver
        self.wait = WebDriverWait(driver, wait_time)

    def find_element(self, locator, wait_condition=EC.presence_of_element_located):
        return self.wait.until(wait_condition(locator))

    def find_elements(self, locator):
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def get_clickable_element(self, locator):
        return self.wait.until(EC.element_to_be_clickable(locator))

    def click_element(self, locator):
        element = self.get_clickable_element(locator)
        element.click()

    def get_sign_in_button(self):
        try:
            return self.wait.until(
                EC.element_to_be_clickable(self.sign_in_button_locator)
            )
        except Exception:
            pass

        try:
            return WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable(self.sign_in_button_alt_locator)
            )
        except Exception:
            raise AssertionError(
                "Could not find sign in button using any locator:\n"
                f"1. {self.sign_in_button_locator}\n"
                f"2. {self.sign_in_button_alt_locator}"
            )

    def click_sign_in(self):
        button = self.get_sign_in_button()
        button.click()

    def get_events_link(self):
        return self.find_element(self.events_link_locator)

    def navigate_to_events(self):
        self.get_events_link().click()
