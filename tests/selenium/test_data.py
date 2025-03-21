"""
Test data and fixtures for Selenium tests
"""

# Sample task data for testing
SAMPLE_TASKS = [
    {
        "title": "Complete project documentation",
        "description": "Update all documentation for the current sprint",
        "status": "In Progress",
        "assignee": "John Doe",
        "dueDate": "2025-04-15"
    },
    {
        "title": "Fix login page UI issues",
        "description": "Address responsive design issues on the login page",
        "status": "New",
        "assignee": "Jane Smith",
        "dueDate": "2025-04-10"
    },
    {
        "title": "Implement user profile settings",
        "description": "Create UI for user profile customization",
        "status": "Completed",
        "assignee": "Mike Johnson",
        "dueDate": "2025-03-30"
    }
]

# Test users for different scenarios
TEST_USERS = {
    "admin": {
        "username": "admin@example.com",
        "password": "AdminPass123!",
        "role": "admin"
    },
    "regular": {
        "username": "user@example.com",
        "password": "UserPass123!",
        "role": "user"
    },
    "viewer": {
        "username": "viewer@example.com",
        "password": "ViewerPass123!",
        "role": "viewer"
    }
}

# Test environment configurations
TEST_ENVIRONMENTS = {
    "local": {
        "base_url": "http://localhost:3000",
        "api_url": "http://localhost:5000",
        "use_real_backend": True
    },
    "dev": {
        "base_url": "https://dev.example.com",
        "api_url": "https://api-dev.example.com",
        "use_real_backend": True
    },
    "staging": {
        "base_url": "https://staging.example.com",
        "api_url": "https://api-staging.example.com",
        "use_real_backend": True
    },
    "prod": {
        "base_url": "https://example.com",
        "api_url": "https://api.example.com",
        "use_real_backend": True
    }
}
