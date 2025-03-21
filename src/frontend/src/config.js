// Configuration for the React frontend, AWS Amplify, and Cognito
const config = {
  // API Gateway
  apiGateway: {
    URL: process.env.REACT_APP_API_URL || 'http://localhost:5000/api'
  },
  // AWS Cognito configuration
  cognito: {
    REGION: process.env.REACT_APP_COGNITO_REGION || 'us-east-1',
    USER_POOL_ID: process.env.REACT_APP_USER_POOL_ID,
    APP_CLIENT_ID: process.env.REACT_APP_CLIENT_ID,
    DOMAIN: process.env.REACT_APP_COGNITO_DOMAIN,
    REDIRECT_SIGN_IN: process.env.REACT_APP_REDIRECT_SIGN_IN || 'http://localhost:3000/callback',
    REDIRECT_SIGN_OUT: process.env.REACT_APP_REDIRECT_SIGN_OUT || 'http://localhost:3000/',
    IDENTITY_POOL_ID: process.env.REACT_APP_IDENTITY_POOL_ID
  }
};

export default config;
