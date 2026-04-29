import pytest
from src.pages.events_page import EventsPage
from src.pages.sign_in_page import SignInPage


def test_events_bookmark_add_and_remove(driver, test_email, test_password):
    if not test_email or not test_password:
        pytest.skip("Test credentials not configured in environment variables (TEST_EMAIL, TEST_PASSWORD)")

    driver.get("https://www.greencity.cx.ua/#/greenCity")

    try:
        sign_in_page = SignInPage(driver)
        sign_in_page.login(test_email, test_password)
        print("Successfully logged in")
    except AssertionError as e:
        pytest.fail(f"Login failed: {str(e)}")
    except Exception as e:
        pytest.fail(f"Unexpected error during login: {str(e)}")

    events_page = EventsPage(driver)
    events_page.open()

    # Get first event with flag and bookmark it
    flag = events_page.get_first_favorites_flag()
    event_card, event_title = events_page.get_event_with_flag()
    print(f"Saving event: {event_title}")

    flag.click()
    assert "flag-active" in flag.get_attribute("class"), \
        "Favorites flag should become active after click"
    print(f"Event marked as favorite: {flag.get_attribute('class')}")

    # Refresh and verify bookmark persists
    driver.refresh()
    print("Page refreshed to verify bookmark persistence")

    events_page.open_bookmarks()
    saved_titles = events_page.get_saved_event_titles()
    assert event_title in saved_titles, \
        f"Event '{event_title}' should be found in saved events. Found: {saved_titles}"
    print(f"Event found in bookmarks")

    # Remove bookmark using EventCard component
    events_page.open()
    event_card_obj = events_page.get_event_card_by_title(event_title)

    became_inactive = event_card_obj.toggle_favorite_and_wait()
    assert became_inactive, "Flag should become inactive after click"
    print("Event removed from favorites")

    # Verify event is removed from bookmarks
    events_page.open_bookmarks()
    saved_titles_after = events_page.get_saved_event_titles()
    assert event_title not in saved_titles_after, \
        f"Event '{event_title}' should not be found in saved events after removal"
    print(f"Event successfully removed from bookmarks")
