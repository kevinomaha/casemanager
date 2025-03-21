# Workflow Manager for Case Management System

A robust workflow management system for tracking and managing tasks within a case management context.

## Features

- Create and manage tasks with detailed information
- Update task status and track progress
- Task closure and archiving
- Real-time notifications for status changes
- User assignment and role-based permissions
- Task timeline and audit trail
- AWS Cognito authentication with OIDC

## Project Structure

```
workflow-manager/
├── config/             # Configuration files
├── docs/               # Documentation
├── src/                # Source code
│   ├── auth/           # Authentication modules
│   ├── controllers/    # Business logic
│   ├── frontend/       # React frontend
│   │   ├── public/     # Static assets
│   │   └── src/        # React components
│   ├── models/         # Data models
│   ├── notifications/  # Notification services
│   ├── utils/          # Utilities
│   └── views/          # UI components (legacy)
└── tests/              # Test suite
    ├── integration/    # Integration tests
    ├── ui/             # UI tests (Selenium)
    └── unit/           # Unit tests
```

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js 16+
- AWS account with appropriate permissions
- PostgreSQL database

### Setting up AWS Cognito

1. Create a Cognito User Pool in the AWS Console
    - Go to AWS Console > Cognito > User Pools > Create user pool
    - Follow the wizard to set up basic configuration
    - Set up sign-in options (email, username, etc.)
    - Configure security requirements

2. Configure App Integration
    - Set up a domain name for your Cognito User Pool
    - Create an app client with the following settings:
        - App type: Confidential client
        - Authentication flows: ALLOW_USER_PASSWORD_AUTH, ALLOW_REFRESH_TOKEN_AUTH
        - Enable Cognito Hosted UI
        - Set callback URLs: `http://localhost:3000/callback`
        - Set sign-out URLs: `http://localhost:3000/`
        - Select OAuth 2.0 grant types: Authorization code grant
        - Select OpenID Connect scopes: email, openid, profile

3. Configure App Client Settings for OIDC
    - Ensure "Generate client secret" is enabled for your app client
    - Under "Allowed OAuth Flows," check "Authorization code grant"
    - Under "Allowed OAuth Scopes," check "email," "openid," and "profile"
    - Save changes

4. Note down the following information:
    - User Pool ID
    - App Client ID
    - Cognito Domain
    - AWS Region

### Installation

1. Clone the repository
2. Install backend dependencies: `pip install -r requirements.txt`
3. Install frontend dependencies:
   ```
   cd src/frontend
   npm install
   ```
4. Copy `.env.example` to `.env` and update with your Cognito configuration
5. Set up the database
6. Start the backend: `python src/app.py`
7. Start the frontend: 
   ```
   cd src/frontend
   npm start
   ```

## Development

### Backend Development
- Flask server runs on http://localhost:5000
- API endpoints are available at http://localhost:5000/api/...

### Frontend Development
- React app runs on http://localhost:3000
- Communicates with backend API via proxy configuration

## Testing

Run backend tests with pytest:
```
pytest tests/
```

Run frontend tests:
```
cd src/frontend
npm test
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
