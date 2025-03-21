import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';

const Dashboard = ({ user }) => {
  const [stats, setStats] = useState({
    totalTasks: 0,
    completedTasks: 0,
    pendingTasks: 0
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        // For demo purposes - in a real app, this would fetch actual stats
        setStats({
          totalTasks: 15,
          completedTasks: 8,
          pendingTasks: 7
        });
        setLoading(false);
      } catch (err) {
        setError('Failed to fetch dashboard statistics');
        setLoading(false);
        console.error('Error fetching stats:', err);
      }
    };

    fetchStats();
  }, []);

  if (loading) return <div>Loading dashboard data...</div>;
  if (error) return <div className="error-message">{error}</div>;

  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
        <h1>Dashboard</h1>
        {user && (
          <div className="user-greeting">
            <p>Welcome, {user.profile.given_name || user.profile.email}</p>
          </div>
        )}
      </div>
      
      <div className="stats-container">
        <div className="stat-card">
          <h3>Total Tasks</h3>
          <p className="stat-value">{stats.totalTasks}</p>
        </div>
        
        <div className="stat-card">
          <h3>Completed</h3>
          <p className="stat-value">{stats.completedTasks}</p>
        </div>
        
        <div className="stat-card">
          <h3>Pending</h3>
          <p className="stat-value">{stats.pendingTasks}</p>
        </div>
      </div>
      
      <div className="dashboard-actions">
        <Link to="/tasks" className="action-button">
          View All Tasks
        </Link>
      </div>
    </div>
  );
};

export default Dashboard;
