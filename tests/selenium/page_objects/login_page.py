from selenium.webdriver.common.by import By
from tests.selenium.page_objects.base_page import BasePage
import time

class LoginPage(BasePage):
    """Page object for the login page"""
    
    # URL and locators
    URL = "/"  # Root URL redirects to login when not authenticated
    
    # Locators for login elements
    SIGN_IN_BUTTON = (By.CSS_SELECTOR, "button.login-button")
    
    # Cognito login form elements (will be in an iframe or redirect)
    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    SUBMIT_BUTTON = (By.NAME, "signInSubmitButton")
    
    # Error message locators
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".error-message")
    
    def __init__(self, driver, base_url="http://localhost:3000"):
        super().__init__(driver)
        self.base_url = base_url
    
    def open_login_page(self):
        """Navigate to the login page"""
        self.open(f"{self.base_url}{self.URL}")
        return self
    
    def initiate_login(self):
        """Click the sign-in button to start the login process"""
        self.click_element(*self.SIGN_IN_BUTTON)
        # Wait for redirect or iframe loading
        time.sleep(2)
        return self
    
    def enter_credentials(self, username, password):
        """Enter login credentials"""
        # Switch to iframe if needed (depends on your Cognito implementation)
        # If using redirect flow, this will work directly
        self.enter_text(*self.USERNAME_INPUT, username)
        self.enter_text(*self.PASSWORD_INPUT, password)
        return self
    
    def submit_login(self):
        """Submit the login form"""
        self.click_element(*self.SUBMIT_BUTTON)
        # Wait for redirect back to the application
        time.sleep(3)
        return self
    
    def login(self, username, password):
        """Perform full login flow"""
        self.open_login_page()
        self.initiate_login()
        self.enter_credentials(username, password)
        self.submit_login()
        return self
    
    def get_error_message(self):
        """Get the error message if login fails"""
        if self.is_element_visible(*self.ERROR_MESSAGE):
            return self.get_text(*self.ERROR_MESSAGE)
        return None
