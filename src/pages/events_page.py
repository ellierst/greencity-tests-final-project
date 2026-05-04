from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from src.pages.base_page import BasePage
from src.components.filter_panel import FilterPanel
from src.components.event_card import EventCard
from dotenv import load_dotenv
import allure
import os

load_dotenv()


class EventsPage(BasePage):
    EVENT_PAGE_URL = os.getenv("EVENT_PAGE_URL")
    BOOKMARKS_PAGE_URL = os.getenv("BOOKMARKS_PAGE_URL")

    # View toggle buttons
    list_view_button_locator = (By.XPATH, "//button[@aria-label='list view']")
    table_view_button_locator = (By.XPATH, "//button[@aria-label='table view']")

    # Event cards
    event_cards_locator = (By.CSS_SELECTOR, "mat-card.event-list-item")

    # No results message
    no_results_message_locator = (By.XPATH, "//p[@class='end-page-txt ng-star-inserted']")

    # Favorite flag
    favorites_flag_locator = (By.XPATH, "//span[@class='flag']")

    # Locator for event card that contains a bookmark flag
    event_with_favorites_flag_locator = (By.XPATH, "//mat-card[.//span[@class='flag']]")

    def __init__(self, driver, wait_time=30):
        super().__init__(driver, wait_time)
        self.filter_panel = FilterPanel(driver, wait_time)

    @allure.step("Open Events page")
    def open(self):
        self.driver.get(self.EVENT_PAGE_URL)

    @allure.step("Wait for Events page to load")
    def wait_for_page_loaded(self):
        self.wait.until(EC.visibility_of_element_located(self.event_cards_locator))

    @allure.step("Open Bookmarks page")
    def open_bookmarks(self):
        self.driver.get(self.BOOKMARKS_PAGE_URL)

    @allure.step("Open Type dropdown in filter panel")
    def open_type_dropdown(self):
        return self.filter_panel.open_type_dropdown()

    @allure.step("Select Social type in filter panel")
    def select_social_type(self):
        self.filter_panel.select_social_type()

    @allure.step("Get event cards on the page")
    def get_event_cards(self):
        elements = self.find_elements(self.event_cards_locator)
        return [EventCard(self.driver, element) for element in elements]

    @allure.step("Close filter panel")
    def close_filter(self):
        self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
        self.filter_panel.close_filter()

    @allure.step("Open Date dropdown in filter panel")
    def open_date_dropdown(self):
        self.filter_panel.open_date_dropdown()

    @allure.step("Select date range for October 2020 in filter panel")
    def select_date_range_oct_2020(self):
        self.filter_panel.select_date_range_oct_2020()

    @allure.step("Get no results message element")
    def get_no_results_message(self):
        msg = self.find_element(self.no_results_message_locator)
        assert msg.is_displayed(), "No results message is not displayed"
        return msg

    @allure.step("Close date filter")
    def close_date_filter(self):
        self.filter_panel.close_filter()

    @allure.step("Click list view button")
    def click_list_view(self):
        btn = self.get_clickable_element(self.list_view_button_locator)
        assert btn.is_displayed(), "List view button is not displayed"
        btn.click()
        return btn

    @allure.step("Click table view button")
    def click_table_view(self):
        btn = self.get_clickable_element(self.table_view_button_locator)
        assert btn.is_displayed(), "Table view button is not displayed"
        btn.click()
        return btn

    @allure.step("Wait for list view to become active")
    def wait_for_list_view_active(self, list_view_btn):
        self.wait.until(lambda d: list_view_btn.get_attribute("aria-pressed") == "true")

    @allure.step("Wait for list view to become inactive")
    def wait_for_list_view_inactive(self, list_view_btn):
        self.wait.until(lambda d: list_view_btn.get_attribute("aria-pressed") == "false")

    @allure.step("Get first event card with favorites flag")
    def get_first_favorites_flag(self):
        flag = self.find_element(self.favorites_flag_locator, EC.visibility_of_element_located)
        assert flag.is_displayed(), "Favorites flag is not displayed"
        return flag

    @allure.step("Get event card that contains a bookmark flag and return its title")
    def get_event_with_flag(self):
        card_element = self.find_element(self.event_with_favorites_flag_locator, EC.visibility_of_element_located)
        card = EventCard(self.driver, card_element)
        title = card.get_title()
        return card, title

    @allure.step("Get titles of all saved events in bookmarks")
    def get_saved_event_titles(self):
        cards = self.get_event_cards()
        return [card.get_title() for card in cards]

    @allure.step("Get event card by title")
    def get_event_card_by_title(self, title):
        element = self.find_element(
            (By.XPATH, f"//mat-card[.//p[contains(text(), '{title}')]]")
        )
        return EventCard(self.driver, element)
