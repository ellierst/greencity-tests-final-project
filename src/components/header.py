from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from src.components.base_component import BaseComponent
import allure


class Header(BaseComponent):
    sign_in_button_locator = (By.CSS_SELECTOR, ".header_navigation-menu-right-list > .header_sign-in-link")
    sign_in_button_alt_locator = (By.XPATH, "//a[contains(text(), 'Sign in') or contains(text(), 'Увійти')]")

    def __init__(self, driver, wait_time=30):
        super().__init__(driver, self.sign_in_button_locator, wait_time)

    @allure.step("Click sign in button to open login form")
    def click_sign_in(self):
        try:
            btn = self.wait.until(EC.element_to_be_clickable(self.sign_in_button_locator))
            assert btn.is_displayed(), "Sign in button is not displayed"
            btn.click()
        except Exception:
            # Fallback to alternative locator
            btn = self.wait.until(EC.element_to_be_clickable(self.sign_in_button_alt_locator))
            assert btn.is_displayed(), "Sign in button (alternative) is not displayed"
            btn.click()
