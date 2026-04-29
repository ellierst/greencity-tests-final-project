from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from src.pages.base_page import BasePage


class SignInPage(BasePage):
    email_input_locator = (By.ID, "email")
    password_input_locator = (By.ID, "password")
    submit_button_locator = (By.XPATH, "//button[@class='greenStyle']")
    user_header_locator = (By.ID, "header_user-wrp")

    def login(self, email, password):
        try:
            self.click_sign_in()
        except Exception as e:
            raise AssertionError(f"Failed to click sign in button: {str(e)}")
        
        email_input = self.wait.until(EC.visibility_of_element_located(self.email_input_locator))
        email_input.send_keys(email)
        
        password_input = self.wait.until(EC.visibility_of_element_located(self.password_input_locator))
        password_input.send_keys(password)
        
        submit_button = self.wait.until(EC.element_to_be_clickable(self.submit_button_locator))
        assert submit_button.is_displayed(), "Sign in button is not displayed"
        submit_button.click()
        
        # Wait for login to complete
        self.wait.until(EC.visibility_of_element_located(self.user_header_locator))
