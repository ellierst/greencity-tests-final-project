from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from src.pages.base_page import BasePage
import allure


class SignInPage(BasePage):
    email_input_locator = (By.ID, "email")
    password_input_locator = (By.ID, "password")
    submit_button_locator = (By.XPATH, "//button[@class='greenStyle']")
    user_header_locator = (By.ID, "header_user-wrp")

    @allure.step("Click sign in button to open login form")
    def login(self, email, password):
        try:
            self.click_sign_in()
        except Exception as e:
            raise AssertionError(f"Failed to click sign in button: {str(e)}")

        email_input = self.find_element(self.email_input_locator, EC.visibility_of_element_located)
        email_input.send_keys(email)

        password_input = self.find_element(self.password_input_locator, EC.visibility_of_element_located)
        password_input.send_keys(password)

        submit_button = self.find_element(self.submit_button_locator, EC.element_to_be_clickable)
        assert submit_button.is_displayed(), "Sign in button is not displayed"
        submit_button.click()

    @allure.step("Check if user is logged in by verifying presence of user header")
    def is_logged_in(self):
        try:
            self.find_element(self.user_header_locator, EC.visibility_of_element_located)
            return True
        except Exception:
            return False