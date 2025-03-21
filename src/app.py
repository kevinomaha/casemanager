import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from dotenv import load_dotenv
from src.utils.config import Config
from src.controllers.tasks import tasks_blueprint

# Load environment variables
load_dotenv()

# Create Flask application
app = Flask(__name__)
app.config.from_object(Config)

# Enable CORS
CORS(app, resources={r"/api/*": {"origins": app.config.get('CORS_ALLOWED_ORIGINS', '*')}})

# Setup JWT
jwt = JWTManager(app)

# Register blueprints
app.register_blueprint(tasks_blueprint, url_prefix='/api/tasks')

@app.route('/api/health', methods=['GET'])
def health_check():
    """Simple health check endpoint"""
    return jsonify({
        'status': 'up',
        'message': 'API is running'
    })

@app.route('/api/cognito-config', methods=['GET'])
def cognito_config():
    """
    Endpoint to provide Cognito configuration to the frontend
    This avoids hardcoding these values in the frontend code
    """
    return jsonify({
        'region': app.config.get('COGNITO_REGION'),
        'userPoolId': app.config.get('COGNITO_USER_POOL_ID'),
        'clientId': app.config.get('COGNITO_CLIENT_ID'),
        'domain': app.config.get('COGNITO_DOMAIN'),
        'redirectSignIn': app.config.get('COGNITO_CALLBACK_URL'),
        'redirectSignOut': app.config.get('COGNITO_LOGOUT_URL'),
    })

@app.route('/api/validate-token', methods=['POST'])
def validate_token():
    """
    Endpoint to validate JWT tokens issued by Cognito
    The frontend can call this to verify if a token is still valid
    """
    try:
        data = request.get_json()
        token = data.get('token')
        
        if not token:
            return jsonify({'valid': False, 'error': 'No token provided'}), 400
            
        # In a real implementation, we would verify the token
        # For now, we'll just return success
        # In production, use aws-jwt-verify or other JWT verification libraries
        
        return jsonify({'valid': True})
    except Exception as e:
        return jsonify({'valid': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
