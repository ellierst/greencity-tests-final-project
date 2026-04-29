from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from src.pages.base_page import BasePage


class EventsPage(BasePage):
    URL = "https://www.greencity.cx.ua/#/greenCity/events"
    URL_BOOKMARKS = "https://www.greencity.cx.ua/#/greenCity/events?isBookmark=true&section=events"

    type_dropdown_locator = (By.ID, "mat-select-6")
    social_option_locator = (By.XPATH, "//*[@id='mat-option-11']/span")
    date_dropdown_arrow_locator = (By.XPATH, "//div[@class='mat-mdc-select-arrow']")
    close_filter_button_locator = (By.XPATH, "//div[@class='cross-container']")

    change_year_button_locator = (By.XPATH, "//span[@class='mdc-button__label']")
    year_2020_option_locator = (By.XPATH, "//span[contains(text(), '2020')]")
    month_oct_option_locator = (By.XPATH, "//span[contains(text(), 'ЖОВТ.')]")
    start_day_23_locator = (By.XPATH, "//button//span[contains(text(), '23')]")
    end_day_29_locator = (By.XPATH, "//span[contains(text(), '29')]")
    no_results_message_locator = (By.XPATH, "//p[@class='end-page-txt ng-star-inserted']")

    list_view_button_locator = (By.XPATH, "//button[@aria-label='list view']")
    table_view_button_locator = (By.XPATH, "//button[@aria-label='table view']")

    event_cards_locator = (By.CSS_SELECTOR, "mat-card.event-list-item")
    bookmarked_event_cards_locator = (By.CSS_SELECTOR, "mat-card.event-list-item")

    favorites_flag_locator = (By.XPATH, "//span[@class='flag']")

    def open(self):
        self.driver.get(self.URL)

    def open_bookmarks(self):
        self.driver.get(self.URL_BOOKMARKS)

    def open_type_dropdown(self):
        dropdown = self.wait.until(EC.element_to_be_clickable(self.type_dropdown_locator))
        assert dropdown.is_displayed(), "Type of events dropdown is not displayed"
        dropdown.click()
        return dropdown

    def select_social_type(self):
        option = self.wait.until(EC.element_to_be_clickable(self.social_option_locator))
        assert option.is_displayed(), "Social option is not displayed"
        option.click()

    def get_event_cards(self):
        return self.wait.until(EC.presence_of_all_elements_located(self.event_cards_locator))

    def close_filter(self):
        self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
        close_btn = self.wait.until(EC.element_to_be_clickable(self.close_filter_button_locator))
        assert close_btn.is_displayed(), "Close button is not displayed"
        close_btn.click()

    def open_date_dropdown(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.date_dropdown_arrow_locator))
        assert btn.is_displayed(), "Date dropdown button is not displayed"
        btn.click()

    def select_date_range_oct_2020(self):
        year_btn = self.wait.until(EC.element_to_be_clickable(self.change_year_button_locator))
        assert year_btn.is_displayed(), "Change year button is not displayed"
        year_btn.click()

        year_option = self.wait.until(EC.element_to_be_clickable(self.year_2020_option_locator))
        assert year_option.is_displayed(), "Year 2020 option is not displayed"
        year_option.click()

        month_option = self.wait.until(EC.element_to_be_clickable(self.month_oct_option_locator))
        assert month_option.is_displayed(), "October option is not displayed"
        month_option.click()

        start_day = self.wait.until(EC.element_to_be_clickable(self.start_day_23_locator))
        assert start_day.is_displayed(), "Start day 23 is not displayed"
        start_day.click()

        end_day = self.wait.until(EC.element_to_be_clickable(self.end_day_29_locator))
        assert end_day.is_displayed(), "End day 29 is not displayed"
        end_day.click()

    def get_no_results_message(self):
        self.wait.until(EC.visibility_of_element_located(self.no_results_message_locator))
        msg = self.driver.find_element(*self.no_results_message_locator)
        assert msg.is_displayed(), "Not found message is not displayed"
        return msg

    def close_date_filter(self):
        close_btn = self.wait.until(EC.element_to_be_clickable(self.close_filter_button_locator))
        assert close_btn.is_displayed(), "Close button is not displayed"
        close_btn.click()

    def click_list_view(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.list_view_button_locator))
        assert btn.is_displayed(), "List view button is not displayed"
        btn.click()
        return btn

    def click_table_view(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.table_view_button_locator))
        assert btn.is_displayed(), "Table view button is not displayed"
        btn.click()
        return btn

    def wait_for_list_view_active(self, list_view_btn):
        self.wait.until(lambda d: list_view_btn.get_attribute("aria-pressed") == "true")

    def wait_for_list_view_inactive(self, list_view_btn):
        self.wait.until(lambda d: list_view_btn.get_attribute("aria-pressed") == "false")

    def get_first_favorites_flag(self):
        flag = self.wait.until(EC.visibility_of_element_located(self.favorites_flag_locator))
        assert flag.is_displayed(), "Favorites flag is not displayed"
        return flag

    def get_event_with_flag(self):
        card = self.wait.until(
            EC.visibility_of_element_located((By.XPATH, "//mat-card[.//span[@class='flag']]"))
        )
        title = card.find_element(By.CSS_SELECTOR, ".event-title").text
        return card, title

    def get_saved_event_titles(self):
        cards = self.wait.until(
            EC.presence_of_all_elements_located(self.bookmarked_event_cards_locator)
        )
        return [card.find_element(By.CSS_SELECTOR, ".event-title").text for card in cards]

    def get_event_card_by_title(self, title):
        return self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, f"//mat-card[.//p[contains(text(), '{title}')]]")
            )
        )
