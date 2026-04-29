import pytest
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from dotenv import load_dotenv

load_dotenv()


@pytest.fixture(scope="session")
def browser_options():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    
    # Прибираємо ознаки автоматизації
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    
    # Встановлюємо реальний User-Agent (ОБОВ'ЯЗКОВО)
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    return options

@pytest.fixture
def driver(browser_options):
    driver = webdriver.Chrome(options=browser_options)
    
    # Видаляємо прапорець webdriver з navigator
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
        """
    })
    
    # У headless режимі краще НЕ викликати maximize_window(), 
    # якщо window-size вже задано в options
    yield driver
    driver.quit()

@pytest.fixture
def wait(driver):
    """Create WebDriverWait instance for explicit waits"""
    return WebDriverWait(driver, 10)


@pytest.fixture
def test_email():
    """Get test email from environment variables"""
    email = os.getenv("TEST_EMAIL")
    if not email:
        print("⚠ TEST_EMAIL not set in .env file")
    return email


@pytest.fixture
def test_password():
    """Get test password from environment variables"""
    password = os.getenv("TEST_PASSWORD")
    if not password:
        print("⚠ TEST_PASSWORD not set in .env file")
    return password
