from functools import wraps
from flask import request, jsonify, session, g, current_app
from src.auth.cognito import CognitoAuth

def token_required(f):
    """
    Decorator to require a valid authentication token for API requests
    
    Can be used with:
    1. Session-based authentication (for browser requests)
    2. JWT token passed in the Authorization header (for API requests)
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        # Check for session-based authentication first (for browser requests)
        if 'access_token' in session:
            token = session['access_token']
        else:
            # Check for Bearer token in Authorization header (for API requests)
            auth_header = request.headers.get('Authorization')
            if not auth_header or 'Bearer ' not in auth_header:
                return jsonify({'error': 'Authentication token is missing!'}), 401
            
            token = auth_header.split('Bearer ')[1]
        
        if not token:
            return jsonify({'error': 'Authentication token is missing!'}), 401
        
        # Verify the token
        cognito_auth = CognitoAuth(
            user_pool_id=current_app.config.get('COGNITO_USER_POOL_ID'),
            client_id=current_app.config.get('COGNITO_CLIENT_ID')
        )
        
        decoded_token = cognito_auth.verify_token(token)
        if not decoded_token:
            return jsonify({'error': 'Invalid authentication token!'}), 401
        
        # Store token payload in Flask's g object for use in the route function
        g.user = decoded_token
        
        return f(*args, **kwargs)
    
    return decorated
