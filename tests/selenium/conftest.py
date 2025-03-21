import os
import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.firefox import GeckoDriverManager

# Constants for the application URLs
BASE_URL = os.environ.get("TEST_BASE_URL", "http://localhost:3000")

# Define the fixture for the WebDriver (Chrome by default)
@pytest.fixture(scope="function")
def browser(request):
    # Get browser type from command line arguments or use Chrome as default
    browser_type = request.config.getoption("--browser", default="chrome")
    headless = request.config.getoption("--headless", default=True)
    
    if browser_type.lower() == "chrome":
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
    elif browser_type.lower() == "firefox":
        firefox_options = FirefoxOptions()
        if headless:
            firefox_options.add_argument("--headless")
        
        driver = webdriver.Firefox(
            service=Service(GeckoDriverManager().install()),
            options=firefox_options
        )
    else:
        raise ValueError(f"Unsupported browser type: {browser_type}")
    
    # Set implicit wait time
    driver.implicitly_wait(10)
    
    # Return the WebDriver instance
    yield driver
    
    # Teardown - close the browser
    driver.quit()

# Add command line options for browser type and headless mode
def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", 
                     help="Browser to run tests (chrome or firefox)")
    parser.addoption("--headless", action="store_true", default=True,
                     help="Run browser in headless mode")

# Helper functions that can be used across tests
def wait_for_page_load(driver, timeout=10):
    """Wait for page to load completely"""
    time.sleep(1)  # Small wait to ensure JS events are initialized
    # Wait for document ready state
    end_time = time.time() + timeout
    while time.time() < end_time:
        ready_state = driver.execute_script("return document.readyState")
        if ready_state == "complete":
            return True
        time.sleep(0.5)
    raise TimeoutError("Page load timeout")
