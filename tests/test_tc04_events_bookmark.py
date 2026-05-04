import os
import pytest
from src.pages.events_page import EventsPage
from src.pages.sign_in_page import SignInPage
import allure
from dotenv import load_dotenv

load_dotenv()

@allure.title("TC04: Verify that an authorized user can save an event to bookmarks")
@allure.description("Test verifies that an authorized user can bookmark an event and that the bookmark persists. It also checks that the user can remove the bookmark.")
@allure.tag("events", "bookmark", "favorites")
@allure.severity(allure.severity_level.MINOR)
@allure.issue("https://github.com/ellierst/greencity-tests-final-project/issues/4")
def test_events_bookmark_add_and_remove(driver, test_email, test_password):
    with allure.step("Check if test credentials are available"):
        if not test_email or not test_password:
            pytest.skip("Test credentials not configured in environment variables (TEST_EMAIL, TEST_PASSWORD)")

    with allure.step("Open main page and log in"):
        driver.get(os.getenv("BASE_URL"))

    try:
        with allure.step("Perform login"):
            sign_in_page = SignInPage(driver)
        with allure.step("Enter credentials and submit login form"):
            sign_in_page.login(test_email, test_password)
            assert sign_in_page.is_logged_in(), "Login should be successful with valid credentials"
            print("Login successful")
    except AssertionError as e:
        with allure.step("Login failed"):
            pytest.fail(f"Login failed: {str(e)}")
    except Exception as e:
        with allure.step("Unexpected error during login"):
            pytest.fail(f"Unexpected error during login: {str(e)}")

    with allure.step("Open Events page"):
        events_page = EventsPage(driver)
    with allure.step("Verify Events page is loaded"):
        events_page.open()

    with allure.step("Get first event with bookmark flag"):
        flag = events_page.get_first_favorites_flag()
        assert flag is not None, "No events with bookmark flag found"
        print("Found event with bookmark flag")
    with allure.step("Get event card and title for the event with bookmark flag"):
        event_card, event_title = events_page.get_event_with_flag()
        print(f"Saving event: {event_title}")
        assert event_card is not None, "Event card with bookmark flag should be found"

    with allure.step("Click bookmark flag to save event"):
        flag.click()
        assert "flag-active" in flag.get_attribute("class"), \
            "Favorites flag should become active after click"
        print(f"Event marked as favorite: {flag.get_attribute('class')}")

    with allure.step("Refresh page to verify bookmark persistence"):
        driver.refresh()
        print("Page refreshed to verify bookmark persistence")

    with allure.step("Open bookmarks page"):
        events_page.open_bookmarks()
    with allure.step("Verify bookmarked event is present in bookmarks"):
        saved_titles = events_page.get_saved_event_titles()
        assert event_title in saved_titles, \
            f"Event '{event_title}' should be found in saved events. Found: {saved_titles}"
        print(f"Event found in bookmarks")

    with allure.step("Open Events page again"):
        events_page.open()
    with allure.step("Get event card for the bookmarked event"):
        event_card_obj = events_page.get_event_card_by_title(event_title)

    with allure.step("Click bookmark flag to remove event from bookmarks"):
        became_inactive = event_card_obj.toggle_favorite_and_wait()
        assert became_inactive, "Flag should become inactive after click"
        print("Event removed from favorites")

    with allure.step("Open bookmarks page again"):
        events_page.open_bookmarks()
    with allure.step("Verify event is removed from bookmarks"):
        saved_titles_after = events_page.get_saved_event_titles()
        assert event_title not in saved_titles_after, \
            f"Event '{event_title}' should not be found in saved events after removal"
        print(f"Event successfully removed from bookmarks")
