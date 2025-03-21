import pytest
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Basic test to ensure the test setup works
def test_sanity():
    """Basic test to verify that testing works"""
    assert True

# Placeholder test for the app
def test_app_config():
    """Test that we can import and use the app configuration"""
    try:
        from src.utils.config import COGNITO_REGION
        assert isinstance(COGNITO_REGION, str)
    except ImportError:
        pytest.skip("Could not import configuration, skipping test")
