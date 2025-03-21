from selenium.webdriver.common.by import By
from tests.selenium.page_objects.base_page import BasePage
from selenium.webdriver.support.ui import Select

class TaskDetailPage(BasePage):
    """Page object for the task detail page"""
    
    # URL pattern for task detail
    URL_PATTERN = "/tasks/{task_id}"
    
    # Locators for task detail elements
    TASK_TITLE = (By.CSS_SELECTOR, ".task-title h1")
    TASK_DESCRIPTION = (By.CSS_SELECTOR, ".task-description")
    TASK_STATUS = (By.CSS_SELECTOR, ".task-status")
    TASK_ASSIGNEE = (By.CSS_SELECTOR, ".task-assignee")
    TASK_DUE_DATE = (By.CSS_SELECTOR, ".task-due-date")
    
    # Form elements for editing
    EDIT_BUTTON = (By.CSS_SELECTOR, "button.edit-btn")
    SAVE_BUTTON = (By.CSS_SELECTOR, "button.save-btn")
    CANCEL_BUTTON = (By.CSS_SELECTOR, "button.cancel-btn")
    
    # Form input fields
    TITLE_INPUT = (By.ID, "title")
    DESCRIPTION_INPUT = (By.ID, "description")
    STATUS_SELECT = (By.ID, "status")
    ASSIGNEE_INPUT = (By.ID, "assignee")
    DUE_DATE_INPUT = (By.ID, "dueDate")
    
    # Delete task button
    DELETE_BUTTON = (By.CSS_SELECTOR, "button.delete-btn")
    
    def __init__(self, driver, base_url="http://localhost:3000"):
        super().__init__(driver)
        self.base_url = base_url
    
    def open_task_detail(self, task_id):
        """Navigate to a specific task detail page"""
        url = f"{self.base_url}{self.URL_PATTERN.format(task_id=task_id)}"
        self.open(url)
        return self
    
    def get_task_details(self):
        """Get all task details displayed on the page"""
        details = {}
        
        if self.is_element_visible(*self.TASK_TITLE):
            details["title"] = self.get_text(*self.TASK_TITLE)
        
        if self.is_element_visible(*self.TASK_DESCRIPTION):
            details["description"] = self.get_text(*self.TASK_DESCRIPTION)
        
        if self.is_element_visible(*self.TASK_STATUS):
            details["status"] = self.get_text(*self.TASK_STATUS)
        
        if self.is_element_visible(*self.TASK_ASSIGNEE):
            details["assignee"] = self.get_text(*self.TASK_ASSIGNEE)
        
        if self.is_element_visible(*self.TASK_DUE_DATE):
            details["dueDate"] = self.get_text(*self.TASK_DUE_DATE)
        
        return details
    
    def click_edit(self):
        """Click the edit button to enter edit mode"""
        self.click_element(*self.EDIT_BUTTON)
        return self
    
    def update_title(self, new_title):
        """Update the task title"""
        self.enter_text(*self.TITLE_INPUT, new_title)
        return self
    
    def update_description(self, new_description):
        """Update the task description"""
        self.enter_text(*self.DESCRIPTION_INPUT, new_description)
        return self
    
    def update_status(self, new_status):
        """Update the task status from dropdown"""
        select = Select(self.find_element(*self.STATUS_SELECT))
        select.select_by_visible_text(new_status)
        return self
    
    def save_changes(self):
        """Click the save button to save changes"""
        self.click_element(*self.SAVE_BUTTON)
        return self
    
    def cancel_edit(self):
        """Click the cancel button to discard changes"""
        self.click_element(*self.CANCEL_BUTTON)
        return self
    
    def delete_task(self):
        """Click the delete button to delete the task"""
        self.click_element(*self.DELETE_BUTTON)
        
        # Handle confirmation dialog if present
        try:
            alert = self.driver.switch_to.alert
            alert.accept()
        except:
            pass
            
        return self
