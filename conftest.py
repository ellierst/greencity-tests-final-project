import pytest
import os
import allure
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from dotenv import load_dotenv

load_dotenv()


@pytest.fixture(scope="session")
def browser_options():
    options = webdriver.ChromeOptions()
    #options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    
    # For avoiding detection as automation tool
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    
    # Added user-agent to further reduce chances of detection
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    return options

@pytest.fixture
def driver(browser_options):
    driver = webdriver.Chrome(options=browser_options)
    
    # For avoiding detection as automation tool
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
        """
    })
    
    yield driver
    driver.quit()

@pytest.fixture
def wait(driver):
    return WebDriverWait(driver, 10)


@pytest.fixture
def test_email():
    email = os.getenv("TEST_EMAIL")
    if not email:
        print("TEST_EMAIL not set in .env file")
    return email


@pytest.fixture
def test_password():
    password = os.getenv("TEST_PASSWORD")
    if not password:
        print("TEST_PASSWORD not set in .env file")
    return password


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get("driver")
        if driver is not None:
            png_bytes = driver.get_screenshot_as_png()
            allure.attach(
                png_bytes,
                name="screenshot_on_failure",
                attachment_type=allure.attachment_type.PNG
            )
