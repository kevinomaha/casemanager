import os
import secrets

class Config:
    """Configuration settings for the application"""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_hex(32)
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() in ('true', '1', 't')
    
    # CORS settings
    CORS_ALLOWED_ORIGINS = os.environ.get('CORS_ALLOWED_ORIGINS', 'http://localhost:3000').split(',')
    
    # Database settings
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///workflow_manager.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # AWS Cognito settings
    COGNITO_REGION = os.environ.get('COGNITO_REGION', 'us-east-1')
    COGNITO_USER_POOL_ID = os.environ.get('COGNITO_USER_POOL_ID')
    COGNITO_CLIENT_ID = os.environ.get('COGNITO_CLIENT_ID')
    
    # Cognito OIDC/OAuth Configuration
    COGNITO_DOMAIN = os.environ.get('COGNITO_DOMAIN')
    COGNITO_CALLBACK_URL = os.environ.get('COGNITO_CALLBACK_URL', 'http://localhost:3000/callback')
    COGNITO_LOGOUT_URL = os.environ.get('COGNITO_LOGOUT_URL', 'http://localhost:3000/')
    
    # OIDC Scopes to request
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
