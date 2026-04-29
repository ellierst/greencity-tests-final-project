from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from src.components.base_component import BaseComponent


class EventCard(BaseComponent):
    favorite_flag_locator = (By.CSS_SELECTOR, ".flag")
    favorite_flag_active_locator = (By.CSS_SELECTOR, ".flag-active")

    def __init__(self, driver, card_element):
        self.driver = driver
        self._element = card_element

    @property
    def element(self):
        return self._element

    def get_favorite_flag(self):
        try:
            return self.find_element(*self.favorite_flag_locator)
        except Exception:
            return None

    def is_favorite(self):
        try:
            flag = self.find_element(*self.favorite_flag_active_locator)
            return flag.is_displayed()
        except Exception:
            return False
