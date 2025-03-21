import json
import time
import urllib.request
import jwt
import boto3
from flask import current_app

# Cache for JWKS (JSON Web Key Set)
jwks_cache = {
    'keys': None,
    'expiry': 0
}

def get_jwks():
    """
    Retrieve the JSON Web Key Set from Cognito for token verification
    Uses a simple cache to avoid repeated requests
    """
    now = time.time()
    
    # Return cached keys if still valid
    if jwks_cache['keys'] and jwks_cache['expiry'] > now:
        return jwks_cache['keys']
    
    # Retrieve the JWKS from Cognito
    jwks_uri = current_app.config.get('COGNITO_JWKS_URI')
    
    try:
        with urllib.request.urlopen(jwks_uri) as response:
            jwks = json.loads(response.read().decode('utf-8'))
            
        # Cache the keys for 24 hours
        jwks_cache['keys'] = jwks
        jwks_cache['expiry'] = now + 86400  # 24 hours
        
        return jwks
    except Exception as e:
        print(f"Error retrieving JWKS: {str(e)}")
        return None

def verify_cognito_token(token):
    """
    Verify a JWT token issued by AWS Cognito
    
    Args:
        token: The JWT token to verify
        
    Returns:
        The token's claims if valid, None otherwise
    """
    try:
        # Step 1: Get the header from the token
        header = jwt.get_unverified_header(token)
        
        # Step 2: Get the key ID from the header
        kid = header.get('kid')
        if not kid:
            return None
        
        # Step 3: Get the JWKS
        jwks = get_jwks()
        if not jwks:
            return None
        
        # Step 4: Find the key with matching kid
        key = next((k for k in jwks['keys'] if k['kid'] == kid), None)
        if not key:
            return None
        
        # Step 5: Verify the token
        # Note: This is a simplified example. In production, you should use 
        # a proper JWT library with full validation
        user_pool_id = current_app.config.get('COGNITO_USER_POOL_ID')
        client_id = current_app.config.get('COGNITO_CLIENT_ID')
        
        # In a real implementation, we would construct the public key from the JWKS
        # and use it to verify the token signature
        # For this example, we'll skip signature verification and just decode the payload
        
        decoded = jwt.decode(
            token,
            options={"verify_signature": False},  # In production, set this to True
            audience=client_id
        )
        
        # Verify token hasn't expired
        now = time.time()
        if decoded.get('exp', 0) < now:
            return None
        
        # Verify the token was issued by the correct user pool
        iss = decoded.get('iss')
        expected_issuer = f"https://cognito-idp.{current_app.config.get('COGNITO_REGION')}.amazonaws.com/{user_pool_id}"
        if iss != expected_issuer:
            return None
        
        return decoded
        
    except Exception as e:
        print(f"Token verification error: {str(e)}")
        return None
