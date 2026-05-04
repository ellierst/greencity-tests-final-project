from src.pages.events_page import EventsPage
import allure

@allure.title("TC03: Verify that the events list displays a no results message when no events match the filters")
@allure.description("Test verifies that a no results message is displayed when filtering events yields no matches.")
@allure.tag("events", "filter", "no_results")
@allure.severity(allure.severity_level.NORMAL)
@allure.issue("https://github.com/ellierst/greencity-tests-final-project/issues/3")
def test_events_no_results_message(driver):
    with allure.step("Open Events page"):
        events_page = EventsPage(driver)
    with allure.step("Verify Events page is loaded"):
        events_page.open()

    with allure.step("Open date filter"):
        events_page.open_date_dropdown()
    with allure.step("Select date range that yields no results"):
        events_page.select_date_range_oct_2020()

    with allure.step("Verify no results message is displayed"):
        no_results_msg = events_page.get_no_results_message()
        assert no_results_msg.is_displayed(), "No results message should be displayed"
        assert len(no_results_msg.text.strip()) > 0, "No results message should not be empty"

    with allure.step("Close date filter"):
        events_page.close_date_filter()
