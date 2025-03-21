import pytest
import os
import time
from tests.selenium.page_objects.login_page import LoginPage
from tests.selenium.page_objects.tasks_list_page import TasksListPage
from tests.selenium.page_objects.task_detail_page import TaskDetailPage

# Get test credentials from environment variables
TEST_USERNAME = os.environ.get("TEST_USERNAME", "test@example.com")
TEST_PASSWORD = os.environ.get("TEST_PASSWORD", "TestPassword1!")
BASE_URL = os.environ.get("TEST_BASE_URL", "http://localhost:3000")

@pytest.mark.usefixtures("browser")
class TestTasks:
    """Test class for tasks functionality"""
    
    @pytest.fixture(autouse=True)
    def login_first(self, browser):
        """Login before each test"""
        # Skip login in CI environment without real credentials
        if os.environ.get("CI") and TEST_USERNAME == "test@example.com":
            pytest.skip("Skipping in CI environment without real credentials")
            
        login_page = LoginPage(browser, BASE_URL)
        login_page.login(TEST_USERNAME, TEST_PASSWORD)
    
    def test_tasks_list_page_loads(self, browser):
        """Test that the tasks list page loads correctly"""
        tasks_page = TasksListPage(browser, BASE_URL)
        tasks_page.open_tasks_page()
        
        # Verify that either tasks list or 'no tasks' message is displayed
        assert tasks_page.is_tasks_list_displayed() or \
              tasks_page.is_no_tasks_message_displayed(), \
              "Neither tasks list nor 'no tasks' message is displayed"
    
    def test_task_creation_flow(self, browser):
        """Test task creation flow"""
        tasks_page = TasksListPage(browser, BASE_URL)
        tasks_page.open_tasks_page()
        
        # Store initial task count
        initial_count = tasks_page.get_task_count()
        
        # Click create task button
        tasks_page.click_create_task()
        
        # Now we should be on the task creation form
        # This might be a separate page or a modal dialog
        # For this test, we'll assume it's a detail page with empty fields
        task_detail = TaskDetailPage(browser, BASE_URL)
        
        # Fill in task details
        test_title = f"Test Task {time.time()}"
        task_detail.update_title(test_title)
        task_detail.update_description("This is a test task created by Selenium")
        task_detail.update_status("In Progress")
        
        # Save the new task
        task_detail.save_changes()
        
        # We should be redirected back to the tasks list
        # Wait a moment for the redirect and page load
        time.sleep(2)
        
        # Refresh the page to ensure we get the latest data
        tasks_page.open_tasks_page()
        
        # Verify that task count increased
        new_count = tasks_page.get_task_count()
        
        # If using a real backend with persistence:
        if os.environ.get("USE_REAL_BACKEND", "false").lower() == "true":
            assert new_count > initial_count, \
                f"Task count did not increase after creation. Was {initial_count}, now {new_count}"
            
            # Verify that the new task appears in the list
            task_titles = tasks_page.get_task_titles()
            assert test_title in task_titles, f"New task '{test_title}' not found in task list"
    
    def test_task_detail_view(self, browser):
        """Test viewing task details"""
        tasks_page = TasksListPage(browser, BASE_URL)
        tasks_page.open_tasks_page()
        
        # Skip this test if no tasks exist
        if tasks_page.is_no_tasks_message_displayed():
            pytest.skip("No tasks available to test detail view")
        
        # Click on the first task in the list
        tasks_page.click_on_task(0)
        
        # Now we should be on the task detail page
        task_detail = TaskDetailPage(browser, BASE_URL)
        
        # Get task details
        details = task_detail.get_task_details()
        
        # Verify that essential details are present
        assert "title" in details, "Task title not displayed in detail view"
        assert details["title"], "Task title is empty"
