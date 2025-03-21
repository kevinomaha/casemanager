import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from utils.config import (
    CORS_ALLOWED_ORIGINS, 
    COGNITO_REGION, 
    COGNITO_USER_POOL_ID, 
    COGNITO_CLIENT_ID,
    COGNITO_DOMAIN,
    COGNITO_CALLBACK_URL,
    COGNITO_LOGOUT_URL,
    COGNITO_SCOPES
)
from utils.cognito_verify import verify_cognito_token
from src.controllers.tasks import tasks_blueprint

# Load environment variables
load_dotenv()

# Create Flask application
app = Flask(__name__)
app.config.from_object(Config)

# Configure CORS
CORS(app, resources={r"/api/*": {"origins": CORS_ALLOWED_ORIGINS}})

# Setup JWT
jwt = JWTManager(app)

# Register blueprints
app.register_blueprint(tasks_blueprint, url_prefix='/api/tasks')

@app.route('/api/health', methods=['GET'])
def health_check():
    """Simple health check endpoint"""
    return jsonify({"status": "healthy"}), 200

@app.route('/api/cognito-config', methods=['GET'])
def get_cognito_config():
    """
    Endpoint to provide Cognito configuration to the frontend
    This avoids hardcoding these values in the frontend code
    """
    config = {
        "region": COGNITO_REGION,
        "userPoolId": COGNITO_USER_POOL_ID,
        "clientId": COGNITO_CLIENT_ID,
        "domain": COGNITO_DOMAIN,
        "callbackUrl": COGNITO_CALLBACK_URL,
        "logoutUrl": COGNITO_LOGOUT_URL,
        "scopes": COGNITO_SCOPES
    }
    return jsonify(config), 200

@app.route('/api/validate-token', methods=['POST'])
def validate_token():
    """
    Endpoint to validate JWT tokens issued by Cognito
    The frontend can call this to verify if a token is still valid
    """
    try:
        token = request.json.get('token')
        if not token:
            return jsonify({"error": "No token provided"}), 400
        
        # Verify the token
        claims = verify_cognito_token(token)
        
        # Return the claims if token is valid
        return jsonify({
            "valid": True,
            "claims": claims
        }), 200
    except Exception as e:
        return jsonify({
            "valid": False,
            "error": str(e)
        }), 401

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
