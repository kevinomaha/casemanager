import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from 'react-oidc-context';

// Components
import Dashboard from './components/Dashboard';
import TasksList from './components/TasksList';
import TaskDetail from './components/TaskDetail';
import Navigation from './components/Navigation';
import ProtectedRoute from './components/ProtectedRoute';

// Main App component
function App() {
  const auth = useAuth();

  // Custom sign out function for Cognito
  const signOutRedirect = () => {
    const clientId = "30o9hu5r46ufq4o1ask25t4bpr";
    const logoutUri = "https://d84l1y8p4kdic.cloudfront.net";
    const cognitoDomain = "https://your-cognito-domain.auth.us-east-2.amazoncognito.com";
    window.location.href = `${cognitoDomain}/logout?client_id=${clientId}&logout_uri=${encodeURIComponent(logoutUri)}`;
  };

  // Handle different auth states
  switch (auth.activeNavigator) {
    case "signinSilent":
      return <div>Signing you in...</div>;
    case "signoutRedirect":
      return <div>Signing you out...</div>;
  }

  if (auth.isLoading) {
    return <div>Loading authentication...</div>;
  }

  if (auth.error) {
    return <div>Authentication error: {auth.error.message}</div>;
  }

  return (
    <Router>
      <div className="App">
        <Navigation signOutRedirect={signOutRedirect} />
        <main>
          <Routes>
            <Route path="/" element={
              auth.isAuthenticated ? (
                <Navigate to="/dashboard" replace />
              ) : (
                <div className="login-container">
                  <h1>Workflow Manager</h1>
                  <p>Please sign in to continue</p>
                  <button onClick={() => auth.signinRedirect()}>
                    Sign In with Cognito
                  </button>
                </div>
              )
            } />
            <Route path="/dashboard" element={
              <ProtectedRoute>
                <Dashboard user={auth.user} />
              </ProtectedRoute>
            } />
            <Route path="/tasks" element={
              <ProtectedRoute>
                <TasksList />
              </ProtectedRoute>
            } />
            <Route path="/tasks/:id" element={
              <ProtectedRoute>
                <TaskDetail />
              </ProtectedRoute>
            } />
            <Route path="/auth-debug" element={
              <ProtectedRoute>
                <div className="auth-debug">
                  <h2>Authentication Debug Information</h2>
                  <p>Hello: {auth.user?.profile.email}</p>
                  <div className="token-info">
                    <h3>ID Token</h3>
                    <pre>{auth.user?.id_token}</pre>
                    
                    <h3>Access Token</h3>
                    <pre>{auth.user?.access_token}</pre>
                    
                    <h3>Refresh Token</h3>
                    <pre>{auth.user?.refresh_token}</pre>
                  </div>
                  <button onClick={() => auth.removeUser()}>Sign out</button>
                  <button onClick={signOutRedirect}>Sign out (Redirect)</button>
                </div>
              </ProtectedRoute>
            } />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
