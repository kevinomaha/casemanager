# Selenium Test Framework for Workflow Manager Frontend

This directory contains Selenium tests for the Workflow Manager frontend application. The tests are organized using the Page Object Model pattern for maintainability and reusability.

## Structure

- `conftest.py` - Contains pytest fixtures and configuration
- `page_objects/` - Contains page object classes for different pages of the application
- `test_*.py` - Test files for different functionalities
- `test_data.py` - Contains test data and fixtures

## Prerequisites

1. Python 3.8 or higher
2. Chrome or Firefox browser
3. The frontend application running (default: http://localhost:3000)
4. The backend API running (default: http://localhost:5000)
5. Webdriver Manager for Python

## Installation

```bash
# Install required packages
pip install -r requirements.txt

# Or specifically for Selenium tests
pip install selenium webdriver-manager pytest
```

## Running the Tests

### Basic Test Run

```bash
# Run all tests
pytest tests/selenium

# Run specific test file
pytest tests/selenium/test_login.py

# Run specific test
pytest tests/selenium/test_login.py::TestLogin::test_successful_login
```

### Running with Different Browsers

```bash
# Run with Chrome (default)
pytest tests/selenium --browser=chrome

# Run with Firefox
pytest tests/selenium --browser=firefox
```

### Non-Headless Mode (for debugging)

```bash
# Run in non-headless mode to see browser actions
pytest tests/selenium --headless=false
```

## Environment Variables

You can configure the tests using the following environment variables:

- `TEST_BASE_URL` - Base URL of the frontend application (default: http://localhost:3000)
- `TEST_USERNAME` - Username for login tests
- `TEST_PASSWORD` - Password for login tests
- `USE_REAL_BACKEND` - Set to "true" to test with real backend, "false" for mock data (default: "false")
- `CI` - Set automatically in CI environments to adjust test behavior

## Setting Up in CI/CD Pipeline

For GitHub Actions, add the following job to your workflow:

```yaml
selenium-tests:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install selenium webdriver-manager pytest
        if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
    - name: Start frontend and backend
      run: |
        # Start your application in background
        npm start &
        # Wait for it to start
        sleep 10
    - name: Run Selenium tests
      run: |
        pytest tests/selenium -v
      env:
        CI: true
        TEST_BASE_URL: http://localhost:3000
```

## Writing New Tests

To add new tests:

1. Create a new page object class if testing a new page
2. Create a new test file or add tests to an existing file
3. Use the provided fixtures and page objects
4. Follow the existing patterns for consistency

## Best Practices

1. Each test should be independent and not rely on other tests
2. Use appropriate waits for elements rather than fixed sleeps
3. Use explicit assertions to validate test outcomes
4. Clean up test data after tests if necessary
5. Make tests robust against small UI changes
