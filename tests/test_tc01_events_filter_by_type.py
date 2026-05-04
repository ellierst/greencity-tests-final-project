from src.pages.events_page import EventsPage
import allure

@allure.title("TC01: Verify that the events list can be filtered by event type")
@allure.description("Test verifies that filtering events by type (e.g., Social) works correctly and displays relevant events.")
@allure.tag("events", "filter", "type")
@allure.severity(allure.severity_level.NORMAL)
@allure.issue("https://github.com/ellierst/greencity-tests-final-project/issues/1")
def test_events_filter_by_type(driver):
    with allure.step("Open Events page"):
        events_page = EventsPage(driver)
        events_page.open()

    with allure.step("Verify Events page is loaded"):
        events_page.wait_for_page_loaded()

    with allure.step("Open Type dropdown"):
        events_page.open_type_dropdown()
    with allure.step("Select Social type"):
        events_page.select_social_type()

    with allure.step("Get event cards and verify they are displayed"):
        event_cards = events_page.get_event_cards()
        assert len(event_cards) > 0, "No posts found after filtering by Social type"

    with allure.step("Verify each event card has at least one Social tag"):
        social_tags = {"Social", "СОЦІАЛЬНИЙ"}
        
        for card in event_cards:
            with allure.step(f"Check event card with title: '{card.get_title()}'"):
                tags = card.get_tags()
                assert len(tags) > 0, "No tags found in event card"
            
            with allure.step(f"Verify at least one Social tag is present in the event card: {card.has_any_tag(social_tags)}"):
                assert card.has_any_tag(social_tags), \
                    f"No Social tag in event card. Found tags: {tags}"

    with allure.step("Close filter"):
        events_page.close_filter()
