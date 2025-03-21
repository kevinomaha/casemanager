import os
import json
import requests
import base64
import boto3
import jwt
from urllib.parse import urlencode

class CognitoAuth:
    """
    Handles AWS Cognito authentication flows
    """
    
    def __init__(self, user_pool_id, client_id, client_secret=None, redirect_uri=None):
        """
        Initialize Cognito Authentication
        
        Args:
            user_pool_id: AWS Cognito User Pool ID
            client_id: AWS Cognito App Client ID
            client_secret: AWS Cognito App Client Secret (if available)
            redirect_uri: Callback URL for authorization code grant flow
        """
        self.user_pool_id = user_pool_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        
        # Extract region from user pool ID
        self.region = user_pool_id.split('_')[0]
        
        # Cognito domain
        self.domain = os.environ.get('COGNITO_DOMAIN')
        
        # Initialize Cognito Identity Provider client
        self.client = boto3.client('cognito-idp', region_name=self.region)
    
    def get_auth_url(self):
        """
        Generate the authorization URL for Cognito hosted UI
        
        Returns:
            The authorization URL to redirect users to
        """
        params = {
            'client_id': self.client_id,
            'response_type': 'code',
            'scope': 'openid email profile',
            'redirect_uri': self.redirect_uri
        }
        
        return f'https://{self.domain}/oauth2/authorize?{urlencode(params)}'
    
    def exchange_code_for_tokens(self, code):
        """
        Exchange authorization code for access, ID, and refresh tokens
        
        Args:
            code: Authorization code received from Cognito
            
        Returns:
            Dictionary containing tokens or error information
        """
        token_endpoint = f'https://{self.domain}/oauth2/token'
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        # Add authorization header if client secret is available
        if self.client_secret:
            auth_string = f"{self.client_id}:{self.client_secret}"
            encoded_auth = base64.b64encode(auth_string.encode()).decode()
            headers['Authorization'] = f'Basic {encoded_auth}'
        
        data = {
            'grant_type': 'authorization_code',
            'client_id': self.client_id,
            'code': code,
            'redirect_uri': self.redirect_uri
        }
        
        try:
            response = requests.post(token_endpoint, headers=headers, data=data)
            return response.json()
        except Exception as e:
            return {'error': str(e)}
    
    def refresh_tokens(self, refresh_token):
        """
        Use refresh token to get new access and ID tokens
        
        Args:
            refresh_token: The refresh token from previous authentication
            
        Returns:
            Dictionary containing new tokens or error information
        """
        token_endpoint = f'https://{self.domain}/oauth2/token'
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        # Add authorization header if client secret is available
        if self.client_secret:
            auth_string = f"{self.client_id}:{self.client_secret}"
            encoded_auth = base64.b64encode(auth_string.encode()).decode()
            headers['Authorization'] = f'Basic {encoded_auth}'
        
        data = {
            'grant_type': 'refresh_token',
            'client_id': self.client_id,
            'refresh_token': refresh_token
        }
        
        try:
            response = requests.post(token_endpoint, headers=headers, data=data)
            return response.json()
        except Exception as e:
            return {'error': str(e)}
    
    def verify_token(self, token):
        """
        Verify the JWT token issued by Cognito
        
        Args:
            token: The JWT token to verify
            
        Returns:
            The decoded token payload if valid, otherwise None
        """
        try:
            # This is a simplified verification - in production, proper JWT verification
            # should be implemented with keys from the jwks_uri endpoint
            decoded = jwt.decode(
                token,
                options={"verify_signature": False},
                algorithms=["RS256"],
                audience=self.client_id
            )
            return decoded
        except Exception as e:
            print(f"Token verification error: {str(e)}")
            return None
    
    def get_user_info(self, access_token):
        """
        Get user information using the access token
        
        Args:
            access_token: The access token from authentication
            
        Returns:
            Dictionary containing user information or error information
        """
        try:
            # Option 1: Use the Cognito User Info endpoint
            userinfo_endpoint = f'https://{self.domain}/oauth2/userInfo'
            headers = {
                'Authorization': f'Bearer {access_token}'
            }
            response = requests.get(userinfo_endpoint, headers=headers)
            
            if response.status_code == 200:
                return response.json()
            
            # Option 2: If userinfo endpoint fails, try using the Cognito API
            response = self.client.get_user(
                AccessToken=access_token
            )
            
            # Transform the response to a more usable format
            user_attributes = {attr['Name']: attr['Value'] for attr in response['UserAttributes']}
            return user_attributes
            
        except Exception as e:
            return {'error': str(e)}
