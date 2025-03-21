from selenium.webdriver.common.by import By
from tests.selenium.page_objects.base_page import BasePage

class TasksListPage(BasePage):
    """Page object for the tasks list page"""
    
    # URL and locators
    URL = "/tasks"
    
    # Locators for tasks list elements
    TASKS_HEADER = (By.CSS_SELECTOR, "h1")
    TASKS_LIST = (By.CSS_SELECTOR, ".tasks-list")
    TASK_ITEMS = (By.CSS_SELECTOR, ".task-item")
    
    # Task creation elements
    CREATE_TASK_BUTTON = (By.CSS_SELECTOR, "button.create-task-btn")
    
    # Filtering elements
    FILTER_INPUT = (By.CSS_SELECTOR, "input.filter-input")
    FILTER_BUTTON = (By.CSS_SELECTOR, "button.filter-btn")
    
    # No tasks message
    NO_TASKS_MESSAGE = (By.CSS_SELECTOR, ".no-tasks-message")
    
    def __init__(self, driver, base_url="http://localhost:3000"):
        super().__init__(driver)
        self.base_url = base_url
    
    def open_tasks_page(self):
        """Navigate to the tasks list page"""
        self.open(f"{self.base_url}{self.URL}")
        return self
    
    def get_task_count(self):
        """Get the number of tasks in the list"""
        tasks = self.find_elements(*self.TASK_ITEMS)
        return len(tasks)
    
    def get_task_titles(self):
        """Get all task titles from the list"""
        tasks = self.find_elements(*self.TASK_ITEMS)
        titles = []
        
        for task in tasks:
            try:
                title_element = task.find_element(By.CSS_SELECTOR, ".task-title")
                titles.append(title_element.text)
            except:
                pass
                
        return titles
    
    def click_on_task(self, index=0):
        """Click on a task at the specified index"""
        tasks = self.find_elements(*self.TASK_ITEMS)
        
        if index < len(tasks):
            tasks[index].click()
        else:
            raise IndexError(f"Task at index {index} does not exist")
            
        return self
    
    def click_create_task(self):
        """Click the create task button"""
        self.click_element(*self.CREATE_TASK_BUTTON)
        return self
    
    def filter_tasks(self, filter_text):
        """Filter tasks by entering text in the filter input"""
        self.enter_text(*self.FILTER_INPUT, filter_text)
        self.click_element(*self.FILTER_BUTTON)
        return self
    
    def is_no_tasks_message_displayed(self):
        """Check if the 'no tasks' message is displayed"""
        return self.is_element_visible(*self.NO_TASKS_MESSAGE)
    
    def is_tasks_list_displayed(self):
        """Check if the tasks list is displayed"""
        return self.is_element_visible(*self.TASKS_LIST)
