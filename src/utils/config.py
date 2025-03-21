import os
import secrets
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration settings for the application"""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key')
    DEBUG = os.environ.get('FLASK_ENV') == 'development'
    
    # CORS settings
    CORS_ALLOWED_ORIGINS = os.environ.get('CORS_ALLOWED_ORIGINS', 'http://localhost:3000').split(',')
    
    # Database settings
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///workflow.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # AWS Cognito settings
    COGNITO_REGION = os.environ.get('COGNITO_REGION', 'us-east-2')
    COGNITO_USER_POOL_ID = os.environ.get('COGNITO_USER_POOL_ID', 'us-east-2_VTDzJDBPV')
    COGNITO_CLIENT_ID = os.environ.get('COGNITO_CLIENT_ID', '30o9hu5r46ufq4o1ask25t4bpr')
    COGNITO_DOMAIN = os.environ.get('COGNITO_DOMAIN', 'your-cognito-domain.auth.us-east-2.amazoncognito.com')
    COGNITO_CALLBACK_URL = os.environ.get('COGNITO_CALLBACK_URL', 'https://d84l1y8p4kdic.cloudfront.net')
    COGNITO_LOGOUT_URL = os.environ.get('COGNITO_LOGOUT_URL', 'https://d84l1y8p4kdic.cloudfront.net')
    
    # Cognito OIDC/OAuth Configuration
    COGNITO_SCOPES = os.environ.get('COGNITO_SCOPES', 'openid email profile').split(' ')
    
    # Response type - using authorization code flow for security
    COGNITO_RESPONSE_TYPE = 'code'
    
    # JWT Configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or secrets.token_hex(32)
    JWT_TOKEN_LOCATION = ['headers']
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'
    
    # Cognito OIDC endpoints (constructed from domain)
    @property
    def COGNITO_AUTHORIZATION_ENDPOINT(self):
        return f"https://{self.COGNITO_DOMAIN}/oauth2/authorize"
    
    @property
    def COGNITO_TOKEN_ENDPOINT(self):
        return f"https://{self.COGNITO_DOMAIN}/oauth2/token"
    
    @property
    def COGNITO_USERINFO_ENDPOINT(self):
        return f"https://{self.COGNITO_DOMAIN}/oauth2/userInfo"
    
    @property
    def COGNITO_JWKS_URI(self):
        return f"https://cognito-idp.{self.COGNITO_REGION}.amazonaws.com/{self.COGNITO_USER_POOL_ID}/.well-known/jwks.json"
