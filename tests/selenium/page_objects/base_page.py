from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class BasePage:
    """Base class for all page objects"""
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def open(self, url):
        """Navigate to a specific page"""
        self.driver.get(url)
    
    def find_element(self, by, value, timeout=10):
        """Find an element on the page with explicit wait"""
        try:
            element = self.wait.until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            raise NoSuchElementException(
                f"Element not found with {by}={value} after {timeout} seconds"
            )
    
    def find_elements(self, by, value, timeout=10):
        """Find multiple elements on the page with explicit wait"""
        try:
            elements = self.wait.until(
                EC.presence_of_all_elements_located((by, value))
            )
            return elements
        except TimeoutException:
            return []
    
    def click_element(self, by, value):
        """Click an element on the page"""
        element = self.find_element(by, value)
        element.click()
    
    def enter_text(self, by, value, text):
        """Enter text into an input field"""
        element = self.find_element(by, value)
        element.clear()
        element.send_keys(text)
    
    def get_text(self, by, value):
        """Get text from an element"""
        element = self.find_element(by, value)
        return element.text
    
    def is_element_visible(self, by, value, timeout=5):
        """Check if an element is visible on the page"""
        try:
            self.wait.until(EC.visibility_of_element_located((by, value)))
            return True
        except TimeoutException:
            return False
    
    def wait_for_element_clickable(self, by, value, timeout=10):
        """Wait for an element to be clickable"""
        self.wait = WebDriverWait(self.driver, timeout)
        return self.wait.until(EC.element_to_be_clickable((by, value)))
        
    def wait_for_url_contains(self, text, timeout=10):
        """Wait for URL to contain specific text"""
        self.wait = WebDriverWait(self.driver, timeout)
        return self.wait.until(EC.url_contains(text))
