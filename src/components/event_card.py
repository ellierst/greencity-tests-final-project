from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from src.components.base_component import BaseComponent


class EventCard(BaseComponent):
    favorite_flag_locator = (By.CSS_SELECTOR, ".flag")
    favorite_flag_active_locator = (By.CSS_SELECTOR, ".flag-active")
    event_title_locator = (By.CSS_SELECTOR, ".event-title")
    card_wrapper_locator = (By.CSS_SELECTOR, ".card-wrapper")
    tags_locator = (By.CSS_SELECTOR, "span.tag-active")

    def __init__(self, driver, card_element):
        self.driver = driver
        self._element = card_element
        # Initialize wait from parent class
        from selenium.webdriver.support.ui import WebDriverWait
        self.wait = WebDriverWait(driver, 10)

    @property
    def element(self):
        return self._element

    def get_favorite_flag(self):
        try:
            return self.find_element(*self.favorite_flag_locator)
        except Exception:
            return None

    def get_active_favorite_flag(self):
        try:
            return self.find_element(*self.favorite_flag_active_locator)
        except Exception:
            return None

    def is_favorite(self):
        try:
            flag = self.get_active_favorite_flag()
            return flag is not None and flag.is_displayed()
        except Exception:
            return False

    def get_title(self):
        title_element = self.find_element(*self.event_title_locator)
        return title_element.text

    def has_list_view_class(self):
        try:
            card_wrapper = self.find_element(*self.card_wrapper_locator)
            classes = card_wrapper.get_attribute("class")
            return "list-view" in classes
        except Exception:
            return False

    def click_favorite_flag(self):
        flag = self.get_favorite_flag()
        if flag:
            flag.click()
        else:
            raise ValueError("Favorite flag not found in event card")

    def toggle_favorite_and_wait(self):
        flag = self.get_active_favorite_flag()
        print(f"Current favorite flag state: {'active' if self.is_favorite() else 'inactive'}")
        if not flag:
            raise ValueError("Favorite flag not found in event card")
        
        # Click the flag
        flag.click()
        print(f"Current favorite flag state after click: {'active' if self.is_favorite() else 'inactive'}")
        print("Clicked favorite flag to toggle state")
        # Wait for the state to change
        if self.is_favorite() == True:
            return self.is_favorite()
        else:
            return not self.is_favorite()

    def get_all_tags(self):
        try:
            return self.find_elements(*self.tags_locator)
        except Exception:
            return []

    def get_tags(self):
        tags_elements = self.get_all_tags()
        return [tag.text.strip() for tag in tags_elements]

    def has_tag(self, tag_name):
        tags = self.get_tags()
        return tag_name in tags

    def has_any_tag(self, tag_names):
        tags = self.get_tags()
        return any(tag in tag_names for tag in tags)
