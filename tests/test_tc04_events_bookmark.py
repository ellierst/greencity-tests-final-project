import pytest
from selenium.webdriver.common.by import By
from src.pages.events_page import EventsPage
from src.pages.sign_in_page import SignInPage


def test_events_bookmark_add_and_remove(driver, test_email, test_password):
    if not test_email or not test_password:
        pytest.skip("Test credentials not configured in environment variables (TEST_EMAIL, TEST_PASSWORD)")

    driver.get("https://www.greencity.cx.ua/#/greenCity")
    
    driver.implicitly_wait(5)

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

    flag = events_page.get_first_favorites_flag()
    _, event_title = events_page.get_event_with_flag()
    print(f"Saving event: {event_title}")

    flag.click()
    assert "flag-active" in flag.get_attribute("class"), \
        "Favorites flag should become active after click"
    print(f"Event marked as favorite {flag.get_attribute('class')}")
    driver.refresh()

    events_page.open_bookmarks()
    saved_titles = events_page.get_saved_event_titles()
    assert event_title in saved_titles, \
        f"Event '{event_title}' should be found in saved events. Found: {saved_titles}"
    print(f"Event found in bookmarks")

    events_page.open()
    event_card = events_page.get_event_card_by_title(event_title)
    active_flag = event_card.find_element(By.CSS_SELECTOR, ".flag-active")
    assert active_flag.is_displayed(), "Active flag should be displayed on the event card"
    active_flag.click()
    
    events_page.wait.until(lambda d: "flag-active" not in active_flag.get_attribute("class"))
    assert "flag-active" not in active_flag.get_attribute("class"), \
        "Favorites flag should become inactive after click"
    print("Event removed from favorites")

    events_page.open_bookmarks()
    saved_titles_after = events_page.get_saved_event_titles()
    assert event_title not in saved_titles_after, \
        f"Event '{event_title}' should not be found in saved events after removal"
    print(f"Event successfully removed from bookmarks")
