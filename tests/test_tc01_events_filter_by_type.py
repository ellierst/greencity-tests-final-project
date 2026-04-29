"""
Test Case TC_01: Events filter by type
Verifies that filtering events by type (Social) displays only events with the Social tag
"""

from selenium.webdriver.common.by import By
from src.pages.events_page import EventsPage


def test_events_filter_by_type(driver):
    events_page = EventsPage(driver)
    events_page.open()

    # Open and select type filter
    events_page.open_type_dropdown()
    events_page.select_social_type()

    # Get all event cards and verify they have Social tag
    posts = events_page.get_event_cards()
    assert len(posts) > 0, "No posts found after filtering by Social type"

    for post in posts:
        tags = post.find_elements(By.CSS_SELECTOR, "span.tag-active")
        assert len(tags) > 0, f"No tags found in post"
        assert any(tag.text.strip() in {"Social", "СОЦІАЛЬНИЙ"} for tag in tags), \
            f"No Social tag in post. Found tags: {[t.text for t in tags]}"

    # Close filter
    events_page.close_filter()
