import React, { useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { Auth } from 'aws-amplify';

const Callback = ({ setIsAuthenticated }) => {
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    // Handle the OAuth callback
    async function handleCallback() {
      try {
        // Get the code from the URL
        const urlParams = new URLSearchParams(location.search);
        const code = urlParams.get('code');

        if (code) {
          // Exchange the code for tokens
          await Auth.federatedSignIn();
          setIsAuthenticated(true);
          navigate('/dashboard');
        }
      } catch (error) {
        console.error('Error handling callback:', error);
        navigate('/');
      }
    }
    
    handleCallback();
  }, [location, navigate, setIsAuthenticated]);

  return (
    <div className="callback-container">
      <div className="callback-content">
        <h2>Logging you in...</h2>
        <div className="loader"></div>
      </div>
    </div>
  );
};

export default Callback;
