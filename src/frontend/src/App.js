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
        <Navigation />
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
              <ProtectedRoute isAuthenticated={auth.isAuthenticated}>
                <Dashboard />
              </ProtectedRoute>
            } />
            <Route path="/tasks" element={
              <ProtectedRoute isAuthenticated={auth.isAuthenticated}>
                <TasksList />
              </ProtectedRoute>
            } />
            <Route path="/tasks/:id" element={
              <ProtectedRoute isAuthenticated={auth.isAuthenticated}>
                <TaskDetail />
              </ProtectedRoute>
            } />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
