import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Application settings
DEBUG = os.environ.get('FLASK_ENV') == 'development'
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key')

# Database settings
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///workflow.db')
SQLALCHEMY_DATABASE_URI = DATABASE_URL
SQLALCHEMY_TRACK_MODIFICATIONS = False

# CORS settings
CORS_ALLOWED_ORIGINS = os.environ.get('CORS_ALLOWED_ORIGINS', 'http://localhost:3000').split(',')

# AWS Cognito settings
COGNITO_REGION = os.environ.get('COGNITO_REGION', 'us-east-2')
COGNITO_USER_POOL_ID = os.environ.get('COGNITO_USER_POOL_ID', 'us-east-2_VTDzJDBPV')
COGNITO_CLIENT_ID = os.environ.get('COGNITO_CLIENT_ID', '30o9hu5r46ufq4o1ask25t4bpr')
COGNITO_DOMAIN = os.environ.get('COGNITO_DOMAIN', 'your-cognito-domain.auth.us-east-2.amazoncognito.com')
COGNITO_CALLBACK_URL = os.environ.get('COGNITO_CALLBACK_URL', 'https://d84l1y8p4kdic.cloudfront.net')
COGNITO_LOGOUT_URL = os.environ.get('COGNITO_LOGOUT_URL', 'https://d84l1y8p4kdic.cloudfront.net')

# OIDC Scopes to request
COGNITO_SCOPES = os.environ.get('COGNITO_SCOPES', 'openid email profile').split(' ')
