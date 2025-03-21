from selenium.webdriver.common.by import By
from tests.selenium.page_objects.base_page import BasePage

class AuthDebugPage(BasePage):
    """Page object for the auth debug page"""
    
    # URL and locators
    URL = "/auth-debug"
    
    # Locators for auth debug elements
    PAGE_HEADER = (By.CSS_SELECTOR, "h1")
    USER_INFO_SECTION = (By.CSS_SELECTOR, ".user-info")
    TOKEN_SECTION = (By.CSS_SELECTOR, ".token-info")
    
    # Specific token information
    ACCESS_TOKEN = (By.CSS_SELECTOR, ".access-token")
    ID_TOKEN = (By.CSS_SELECTOR, ".id-token")
    
    # Navigation elements
    DASHBOARD_LINK = (By.LINK_TEXT, "Dashboard")
    
    def __init__(self, driver, base_url="http://localhost:3000"):
        super().__init__(driver)
        self.base_url = base_url
    
    def open_auth_debug_page(self):
        """Navigate to the auth debug page"""
        self.open(f"{self.base_url}{self.URL}")
        return self
    
    def is_user_info_displayed(self):
        """Check if user information is displayed"""
        return self.is_element_visible(*self.USER_INFO_SECTION)
    
    def is_token_info_displayed(self):
        """Check if token information is displayed"""
        return self.is_element_visible(*self.TOKEN_SECTION)
    
    def get_access_token(self):
        """Get the displayed access token"""
        if self.is_element_visible(*self.ACCESS_TOKEN):
            return self.get_text(*self.ACCESS_TOKEN)
        return None
    
    def get_id_token(self):
        """Get the displayed ID token"""
        if self.is_element_visible(*self.ID_TOKEN):
            return self.get_text(*self.ID_TOKEN)
        return None
    
    def navigate_to_dashboard(self):
        """Click the dashboard link to navigate back"""
        self.click_element(*self.DASHBOARD_LINK)
        return self
