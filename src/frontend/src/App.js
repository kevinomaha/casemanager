import React, { useState, useEffect } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { Authenticator } from '@aws-amplify/ui-react';
import { Auth } from 'aws-amplify';
import '@aws-amplify/ui-react/styles.css';

// Components
import Dashboard from './components/Dashboard';
import TasksList from './components/TasksList';
import TaskDetail from './components/TaskDetail';
import Callback from './components/Callback';
import Navigation from './components/Navigation';
import ProtectedRoute from './components/ProtectedRoute';

// Main App component
function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isAuthenticating, setIsAuthenticating] = useState(true);

  useEffect(() => {
    onLoad();
  }, []);

  async function onLoad() {
    try {
      await Auth.currentSession();
      setIsAuthenticated(true);
    } catch (e) {
      if (e !== 'No current user') {
        console.error(e);
      }
    }
    setIsAuthenticating(false);
  }

  if (isAuthenticating) {
    return <div>Loading...</div>;
  }

  return (
    <Authenticator.Provider>
      <div className="App">
        <Navigation isAuthenticated={isAuthenticated} setIsAuthenticated={setIsAuthenticated} />
        <main>
          <Routes>
            <Route path="/" element={
              isAuthenticated ? <Navigate to="/dashboard" /> : <Authenticator />
            } />
            <Route path="/dashboard" element={
              <ProtectedRoute isAuthenticated={isAuthenticated}>
                <Dashboard />
              </ProtectedRoute>
            } />
            <Route path="/tasks" element={
              <ProtectedRoute isAuthenticated={isAuthenticated}>
                <TasksList />
              </ProtectedRoute>
            } />
            <Route path="/tasks/:id" element={
              <ProtectedRoute isAuthenticated={isAuthenticated}>
                <TaskDetail />
              </ProtectedRoute>
            } />
            <Route path="/callback" element={<Callback setIsAuthenticated={setIsAuthenticated} />} />
          </Routes>
        </main>
      </div>
    </Authenticator.Provider>
  );
}

export default App;
