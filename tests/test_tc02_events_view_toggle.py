from selenium.webdriver.common.by import By
from src.pages.events_page import EventsPage
import allure

@allure.title("TC02: Verify that the events list can be switched between grid and list view")
@allure.description("Test verifies that switching between list and table views works correctly.")
@allure.tag("events", "view", "toggle")
@allure.severity(allure.severity_level.MINOR)
@allure.issue("https://github.com/ellierst/greencity-tests-final-project/issues/2")
def test_events_view_toggle(driver):
    with allure.step("Open Events page"):
        events_page = EventsPage(driver)

    with allure.step("Verify Events page is loaded"):
        events_page.open()

    with allure.step("Verify default view is table view"):
        list_view_btn = events_page.click_list_view()
    with allure.step("Verify list view is active"):
        events_page.wait_for_list_view_active(list_view_btn)
        assert list_view_btn.get_attribute("aria-pressed") == "true", \
        "List view button aria-pressed should be 'true'"

    with allure.step("Verify event cards are displayed in list view"):
        event_cards = events_page.get_event_cards()
        for card in event_cards:
            assert card.has_list_view_class(), \
                "Event card should have 'list-view' class when list view is active"

    with allure.step("Switch to table view"):
        events_page.click_table_view()
    with allure.step("Verify table view is active"):
        events_page.wait_for_list_view_inactive(list_view_btn)
        assert list_view_btn.get_attribute("aria-pressed") == "false", \
            "List view button aria-pressed should be 'false' when table view is active"
