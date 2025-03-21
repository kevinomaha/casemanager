import pytest
import os
from tests.selenium.page_objects.login_page import LoginPage
from tests.selenium.page_objects.dashboard_page import DashboardPage
from tests.selenium.page_objects.tasks_list_page import TasksListPage

# Get test credentials from environment variables
TEST_USERNAME = os.environ.get("TEST_USERNAME", "test@example.com")
TEST_PASSWORD = os.environ.get("TEST_PASSWORD", "TestPassword1!")
BASE_URL = os.environ.get("TEST_BASE_URL", "http://localhost:3000")

@pytest.mark.usefixtures("browser")
class TestDashboard:
    """Test class for dashboard functionality"""
    
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
            "Failed to login before dashboard test"
    
    def test_dashboard_displays_stats(self, browser):
        """Test that dashboard displays task statistics"""
        dashboard_page = DashboardPage(browser, BASE_URL)
        
        # Get task statistics from dashboard
        stats = dashboard_page.get_task_stats()
        
        # Verify that stats are displayed (values don't matter, just presence)
        assert "total" in stats, "Total tasks stat not displayed"
        assert "completed" in stats, "Completed tasks stat not displayed"
        assert "pending" in stats, "Pending tasks stat not displayed"
    
    def test_navigation_to_tasks(self, browser):
        """Test navigation from dashboard to tasks page"""
        dashboard_page = DashboardPage(browser, BASE_URL)
        
        # Navigate to tasks page
        dashboard_page.navigate_to_tasks()
        
        # Verify that tasks page is displayed
        tasks_page = TasksListPage(browser, BASE_URL)
        assert tasks_page.is_tasks_list_displayed() or \
              tasks_page.is_no_tasks_message_displayed(), \
              "Tasks page not displayed after navigation"
    
    def test_logout(self, browser):
        """Test logout functionality from dashboard"""
        dashboard_page = DashboardPage(browser, BASE_URL)
        
        # Perform logout
        dashboard_page.logout()
        
        # Verify redirect to login page after logout
        login_page = LoginPage(browser, BASE_URL)
        assert login_page.is_element_visible(*login_page.SIGN_IN_BUTTON), \
            "Login page not displayed after logout"
