from src.pages.events_page import EventsPage


def test_events_filter_by_type(driver):
    events_page = EventsPage(driver)
    events_page.open()

    # Open and select type filter
    events_page.open_type_dropdown()
    events_page.select_social_type()

    # Get all event cards and verify they have Social tag
    event_cards = events_page.get_event_cards()
    assert len(event_cards) > 0, "No posts found after filtering by Social type"

    social_tags = {"Social", "СОЦІАЛЬНИЙ"}
    
    for card in event_cards:
        # Verify card has tags
        tags = card.get_tags()
        assert len(tags) > 0, "No tags found in event card"
        
        # Verify card has at least one Social tag
        assert card.has_any_tag(social_tags), \
            f"No Social tag in event card. Found tags: {tags}"

    # Close filter
    events_page.close_filter()
