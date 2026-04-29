"""
Test Case TC_03: Events no results message
Verifies that "no results" message is displayed when filtering by date range with no matching events
"""

from src.pages.events_page import EventsPage


def test_events_no_results_message(driver):
    events_page = EventsPage(driver)
    events_page.open()

    # Open date filter and select date range
    events_page.open_date_dropdown()
    events_page.select_date_range_oct_2020()

    # Verify no results message is displayed
    no_results_msg = events_page.get_no_results_message()
    assert no_results_msg.is_displayed(), "No results message should be displayed"
    assert len(no_results_msg.text.strip()) > 0, "No results message should not be empty"

    # Close date filter
    events_page.close_date_filter()
