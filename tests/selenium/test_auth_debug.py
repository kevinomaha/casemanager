import pytest
import os
from tests.selenium.page_objects.login_page import LoginPage
from tests.selenium.page_objects.dashboard_page import DashboardPage
from tests.selenium.page_objects.auth_debug_page import AuthDebugPage

# Get test credentials from environment variables
TEST_USERNAME = os.environ.get("TEST_USERNAME", "test@example.com")
TEST_PASSWORD = os.environ.get("TEST_PASSWORD", "TestPassword1!")
BASE_URL = os.environ.get("TEST_BASE_URL", "http://localhost:3000")

@pytest.mark.usefixtures("browser")
class TestAuthDebug:
    """Test class for auth debug page functionality"""
    
    @pytest.fixture(autouse=True)
    def login_first(self, browser):
        """Login before each test"""
        # Skip login in CI environment without real credentials
        if os.environ.get("CI") and TEST_USERNAME == "test@example.com":
            pytest.skip("Skipping in CI environment without real credentials")
            
        login_page = LoginPage(browser, BASE_URL)
        login_page.login(TEST_USERNAME, TEST_PASSWORD)
        
        # Verify that login was successful
        dashboard_page = DashboardPage(browser, BASE_URL)
        assert dashboard_page.is_dashboard_displayed(), \
            "Failed to login before auth debug test"
    
    def test_auth_debug_page_loads(self, browser):
        """Test that the auth debug page loads correctly"""
        auth_debug_page = AuthDebugPage(browser, BASE_URL)
        auth_debug_page.open_auth_debug_page()
        
        # Verify that user info section is displayed
        assert auth_debug_page.is_user_info_displayed(), \
            "User information not displayed on auth debug page"
    
    def test_token_display(self, browser):
        """Test that tokens are displayed on the page"""
        auth_debug_page = AuthDebugPage(browser, BASE_URL)
        auth_debug_page.open_auth_debug_page()
        
        # Verify that token section is displayed
        assert auth_debug_page.is_token_info_displayed(), \
            "Token information not displayed on auth debug page"
        
        # Check if at least one token is displayed
        # (access token or ID token)
        access_token = auth_debug_page.get_access_token()
        id_token = auth_debug_page.get_id_token()
        
        assert access_token or id_token, \
            "Neither access token nor ID token is displayed"
    
    def test_navigation_back_to_dashboard(self, browser):
        """Test navigation from auth debug page back to dashboard"""
        auth_debug_page = AuthDebugPage(browser, BASE_URL)
        auth_debug_page.open_auth_debug_page()
        
        # Navigate back to dashboard
        auth_debug_page.navigate_to_dashboard()
        
        # Verify that dashboard page is displayed
        dashboard_page = DashboardPage(browser, BASE_URL)
        assert dashboard_page.is_dashboard_displayed(), \
            "Dashboard not displayed after navigation from auth debug page"
