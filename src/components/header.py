from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from src.components.base_component import BaseComponent


class Header(BaseComponent):
    sign_in_button_locator = (By.CSS_SELECTOR, ".header_navigation-menu-right-list > .header_sign-in-link")

    def __init__(self, driver):
        self.driver = driver
        from selenium.webdriver.support.ui import WebDriverWait
        self.wait = WebDriverWait(driver, 30)

    def click_sign_in(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.sign_in_button_locator))
        assert btn.is_displayed(), "Sign in button is not displayed"
        btn.click()
