from selenium.webdriver.common.by import By
from tests.selenium.page_objects.base_page import BasePage

class DashboardPage(BasePage):
    """Page object for the dashboard page"""
    
    # URL and locators
    URL = "/dashboard"
    
    # Locators for dashboard elements
    DASHBOARD_HEADER = (By.CSS_SELECTOR, ".dashboard-header h1")
    USER_GREETING = (By.CSS_SELECTOR, ".user-greeting p")
    
    # Stats cards
    TOTAL_TASKS_CARD = (By.CSS_SELECTOR, ".stat-card:nth-child(1) .stat-value")
    COMPLETED_TASKS_CARD = (By.CSS_SELECTOR, ".stat-card:nth-child(2) .stat-value")
    PENDING_TASKS_CARD = (By.CSS_SELECTOR, ".stat-card:nth-child(3) .stat-value")
    
    # Navigation elements
    TASKS_LINK = (By.LINK_TEXT, "Tasks")
    LOGOUT_BUTTON = (By.CSS_SELECTOR, "button.logout-button")
    
    def __init__(self, driver, base_url="http://localhost:3000"):
        super().__init__(driver)
        self.base_url = base_url
    
    def open_dashboard(self):
        """Navigate to the dashboard page"""
        self.open(f"{self.base_url}{self.URL}")
        return self
    
    def get_welcome_message(self):
        """Get the welcome message that includes the user's name"""
        if self.is_element_visible(*self.USER_GREETING):
            return self.get_text(*self.USER_GREETING)
        return None
    
    def get_task_stats(self):
        """Get the task statistics displayed on the dashboard"""
        stats = {}
        
        if self.is_element_visible(*self.TOTAL_TASKS_CARD):
            stats["total"] = self.get_text(*self.TOTAL_TASKS_CARD)
        
        if self.is_element_visible(*self.COMPLETED_TASKS_CARD):
            stats["completed"] = self.get_text(*self.COMPLETED_TASKS_CARD)
        
        if self.is_element_visible(*self.PENDING_TASKS_CARD):
            stats["pending"] = self.get_text(*self.PENDING_TASKS_CARD)
        
        return stats
    
    def navigate_to_tasks(self):
        """Click the Tasks link to navigate to the tasks page"""
        self.click_element(*self.TASKS_LINK)
        return self
    
    def logout(self):
        """Click the logout button"""
        self.click_element(*self.LOGOUT_BUTTON)
        return self
    
    def is_dashboard_displayed(self):
        """Check if the dashboard is displayed correctly"""
        return self.is_element_visible(*self.DASHBOARD_HEADER)
