from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from src.pages.base_page import BasePage
from src.components.filter_panel import FilterPanel
from src.components.event_card import EventCard


class EventsPage(BasePage):
    URL = "https://www.greencity.cx.ua/#/greenCity/events"
    URL_BOOKMARKS = "https://www.greencity.cx.ua/#/greenCity/events?isBookmark=true&section=events"

    # View toggle buttons
    list_view_button_locator = (By.XPATH, "//button[@aria-label='list view']")
    table_view_button_locator = (By.XPATH, "//button[@aria-label='table view']")

    # Event cards
    event_cards_locator = (By.CSS_SELECTOR, "mat-card.event-list-item")

    # No results message
    no_results_message_locator = (By.XPATH, "//p[@class='end-page-txt ng-star-inserted']")

    # Favorite flag
    favorites_flag_locator = (By.XPATH, "//span[@class='flag']")

    def __init__(self, driver, wait_time=30):
        super().__init__(driver, wait_time)
        self.filter_panel = FilterPanel(driver, wait_time)

    def open(self):
        self.driver.get(self.URL)

    def open_bookmarks(self):
        self.driver.get(self.URL_BOOKMARKS)

    def open_type_dropdown(self):
        return self.filter_panel.open_type_dropdown()

    def select_social_type(self):
        self.filter_panel.select_social_type()

    def get_event_cards(self):
        elements = self.find_elements(self.event_cards_locator)
        return [EventCard(self.driver, element) for element in elements]

    def close_filter(self):
        self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
        self.filter_panel.close_filter()

    def open_date_dropdown(self):
        self.filter_panel.open_date_dropdown()

    def select_date_range_oct_2020(self):
        self.filter_panel.select_date_range_oct_2020()

    def get_no_results_message(self):
        msg = self.find_element(self.no_results_message_locator)
        assert msg.is_displayed(), "No results message is not displayed"
        return msg

    def close_date_filter(self):
        self.filter_panel.close_filter()

    def click_list_view(self):
        btn = self.get_clickable_element(self.list_view_button_locator)
        assert btn.is_displayed(), "List view button is not displayed"
        btn.click()
        return btn

    def click_table_view(self):
        btn = self.get_clickable_element(self.table_view_button_locator)
        assert btn.is_displayed(), "Table view button is not displayed"
        btn.click()
        return btn

    def wait_for_list_view_active(self, list_view_btn):
        self.wait.until(lambda d: list_view_btn.get_attribute("aria-pressed") == "true")

    def wait_for_list_view_inactive(self, list_view_btn):
        self.wait.until(lambda d: list_view_btn.get_attribute("aria-pressed") == "false")

    def get_first_favorites_flag(self):
        flag = self.find_element(self.favorites_flag_locator, EC.visibility_of_element_located)
        assert flag.is_displayed(), "Favorites flag is not displayed"
        return flag

    def get_event_with_flag(self):
        card_element = self.find_element(
            (By.XPATH, "//mat-card[.//span[@class='flag']]"),
            EC.visibility_of_element_located
        )
        card = EventCard(self.driver, card_element)
        title = card.get_title()
        return card, title

    def get_saved_event_titles(self):
        cards = self.get_event_cards()
        return [card.get_title() for card in cards]

    def get_event_card_by_title(self, title):
        element = self.find_element(
            (By.XPATH, f"//mat-card[.//p[contains(text(), '{title}')]]")
        )
        return EventCard(self.driver, element)
