import React, { useState, useEffect } from 'react';
import { API, Auth } from 'aws-amplify';
import { Link } from 'react-router-dom';

const Dashboard = () => {
  const [user, setUser] = useState(null);
  const [tasks, setTasks] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function loadUserData() {
      try {
        // Get user information
        const currentUser = await Auth.currentAuthenticatedUser();
        setUser(currentUser);

        // Get tasks data
        const taskData = await API.get('api', '/tasks');
        setTasks(taskData);
        
        setIsLoading(false);
      } catch (err) {
        console.error('Error loading user data:', err);
        setError('Failed to load dashboard data. Please try again.');
        setIsLoading(false);
      }
    }

    loadUserData();
  }, []);

  if (isLoading) {
    return <div className="loader">Loading...</div>;
  }

  if (error) {
    return <div className="error-message">{error}</div>;
  }

  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
        <h1>Welcome, {user?.attributes?.given_name || 'User'}!</h1>
        <p>Your personal workflow dashboard</p>
      </div>

      <div className="dashboard-summary">
        <div className="summary-card">
          <h3>Tasks Assigned</h3>
          <p className="summary-number">{tasks.length}</p>
        </div>
        <div className="summary-card">
          <h3>Tasks in Progress</h3>
          <p className="summary-number">
            {tasks.filter(task => task.status === 'in_progress').length}
          </p>
        </div>
        <div className="summary-card">
          <h3>Completed Tasks</h3>
          <p className="summary-number">
            {tasks.filter(task => task.status === 'completed').length}
          </p>
        </div>
      </div>

      <div className="recent-tasks">
        <div className="section-header">
          <h2>Recent Tasks</h2>
          <Link to="/tasks" className="view-all">View All Tasks</Link>
        </div>
        
        <div className="tasks-list">
          {tasks.slice(0, 5).map(task => (
            <div key={task.id} className="task-item">
              <h3>
                <Link to={`/tasks/${task.id}`}>{task.title}</Link>
              </h3>
              <p className="task-description">{task.description}</p>
              <div className="task-footer">
                <span className={`status-badge ${task.status}`}>{task.status}</span>
              </div>
            </div>
          ))}
          
          {tasks.length === 0 && (
            <p className="no-items-message">No tasks assigned to you.</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
