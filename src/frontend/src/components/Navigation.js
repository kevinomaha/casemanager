import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from 'react-oidc-context';

const Navigation = ({ signOutRedirect }) => {
  const auth = useAuth();

  return (
    <nav className="navbar">
      <div className="logo">
        <Link to="/">Workflow Manager</Link>
      </div>
      <ul className="nav-links">
        {auth.isAuthenticated ? (
          <>
            <li>
              <Link to="/dashboard">Dashboard</Link>
            </li>
            <li>
              <Link to="/tasks">Tasks</Link>
            </li>
            <li>
              <Link to="/auth-debug">Auth Debug</Link>
            </li>
            <li>
              <button 
                onClick={signOutRedirect} 
                className="nav-button"
              >
                Sign Out
              </button>
            </li>
          </>
        ) : (
          <li>
            <button 
              onClick={() => auth.signinRedirect()}
              className="nav-button"
            >
              Sign In
            </button>
          </li>
        )}
      </ul>
    </nav>
  );
};

export default Navigation;
