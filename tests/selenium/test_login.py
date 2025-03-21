import pytest
import os
from tests.selenium.page_objects.login_page import LoginPage
from tests.selenium.page_objects.dashboard_page import DashboardPage

# Get test credentials from environment variables (for security)
TEST_USERNAME = os.environ.get("TEST_USERNAME", "test@example.com")
TEST_PASSWORD = os.environ.get("TEST_PASSWORD", "TestPassword1!")
BASE_URL = os.environ.get("TEST_BASE_URL", "http://localhost:3000")

@pytest.mark.usefixtures("browser")
class TestLogin:
    """Test class for login functionality"""
    
    def test_login_page_loads(self, browser):
        """Test that the login page loads correctly"""
        login_page = LoginPage(browser, BASE_URL)
        login_page.open_login_page()
        
        # Verify that the sign-in button is visible
        assert login_page.is_element_visible(*login_page.SIGN_IN_BUTTON), \
            "Sign-in button is not visible on the login page"
    
    def test_successful_login(self, browser):
        """Test successful login flow with valid credentials"""
        login_page = LoginPage(browser, BASE_URL)
        
        # Skip this test if running in CI environment without real credentials
        if os.environ.get("CI") and TEST_USERNAME == "test@example.com":
            pytest.skip("Skipping in CI environment without real credentials")
        
        # Perform login
        login_page.login(TEST_USERNAME, TEST_PASSWORD)
        
        # Verify redirect to dashboard after login
        dashboard_page = DashboardPage(browser, BASE_URL)
        assert dashboard_page.is_dashboard_displayed(), \
            "Dashboard was not displayed after login"
        
        # Verify user greeting contains username or email
        welcome_message = dashboard_page.get_welcome_message()
        assert welcome_message is not None, "Welcome message not found"
        
        # Extract username from greeting message
        # The format is typically "Welcome, {username}"
        if TEST_USERNAME in welcome_message:
            assert True, "Username found in welcome message"
        else:
            assert "Welcome" in welcome_message, "Welcome message format incorrect"
    
    def test_invalid_login(self, browser):
        """Test login failure with invalid credentials"""
        login_page = LoginPage(browser, BASE_URL)
        
        # Try to login with invalid credentials
        login_page.login("invalid@example.com", "InvalidPassword123!")
        
        # Verify that an error message is displayed
        # This might vary depending on your Cognito implementation
        error_message = login_page.get_error_message()
        if error_message:
            assert "incorrect" in error_message.lower() or \
                   "invalid" in error_message.lower() or \
                   "failed" in error_message.lower(), \
                   "Error message does not indicate invalid credentials"
        else:
            # If no specific error message, check that we're still on login page
            assert login_page.is_element_visible(*login_page.SIGN_IN_BUTTON), \
                "Should still be on login page after failed login"
