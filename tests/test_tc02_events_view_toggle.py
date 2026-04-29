from selenium.webdriver.common.by import By
from src.pages.events_page import EventsPage


def test_events_view_toggle(driver):
    events_page = EventsPage(driver)
    events_page.open()

    # Test list view
    list_view_btn = events_page.click_list_view()
    events_page.wait_for_list_view_active(list_view_btn)

    assert list_view_btn.get_attribute("aria-pressed") == "true", \
        "List view button aria-pressed should be 'true'"

    # Verify posts have list-view class
    event_cards = events_page.get_event_cards()
    for card in event_cards:
        assert card.has_list_view_class(), \
            "Event card should have 'list-view' class when list view is active"

    # Test table view
    events_page.click_table_view()
    events_page.wait_for_list_view_inactive(list_view_btn)

    assert list_view_btn.get_attribute("aria-pressed") == "false", \
        "List view button aria-pressed should be 'false' when table view is active"
