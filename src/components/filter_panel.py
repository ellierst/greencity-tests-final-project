from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from src.components.base_component import BaseComponent
import allure


class FilterPanel(BaseComponent):
    type_dropdown_locator = (By.ID, "mat-select-6")
    social_option_locator = (By.XPATH, "//*[@id='mat-option-11']/span")
    date_dropdown_arrow_locator = (By.XPATH, "//div[@class='mat-mdc-select-arrow']")
    close_filter_button_locator = (By.XPATH, "//div[@class='cross-container']")

    change_year_button_locator = (By.XPATH, "//span[@class='mdc-button__label']")
    year_2020_option_locator = (By.XPATH, "//span[contains(text(), '2020')]")
    month_oct_option_locator = (By.XPATH, "//span[contains(text(), 'ЖОВТ.')]")
    start_day_23_locator = (By.XPATH, "//button//span[contains(text(), '23')]")
    end_day_29_locator = (By.XPATH, "//span[contains(text(), '29')]")

    def __init__(self, driver, wait_time=10):
        super().__init__(driver, self.type_dropdown_locator, wait_time)

    @allure.step("Open Type dropdown in filter panel")
    def open_type_dropdown(self):
        dropdown = self.wait.until(EC.element_to_be_clickable(self.type_dropdown_locator))
        assert dropdown.is_displayed(), "Type dropdown is not displayed"
        dropdown.click()
        return dropdown

    @allure.step("Select Social type in filter panel")
    def select_social_type(self):
        option = self.wait.until(EC.element_to_be_clickable(self.social_option_locator))
        assert option.is_displayed(), "Social option is not displayed"
        option.click()

    @allure.step("Open Date dropdown in filter panel")
    def open_date_dropdown(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.date_dropdown_arrow_locator))
        assert btn.is_displayed(), "Date dropdown button is not displayed"
        btn.click()

    @allure.step("Select date range for October 2020 in filter panel")
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

    @allure.step("Close filter panel")
    def close_filter(self):
        close_btn = self.wait.until(EC.element_to_be_clickable(self.close_filter_button_locator))
        assert close_btn.is_displayed(), "Close button is not displayed"
        close_btn.click()
