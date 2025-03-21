import React, { useState, useEffect } from 'react';
import { API } from 'aws-amplify';
import { Link } from 'react-router-dom';

const TasksList = () => {
  const [tasks, setTasks] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    fetchTasks();
  }, []);

  async function fetchTasks() {
    try {
      setIsLoading(true);
      const tasksData = await API.get('api', '/tasks');
      setTasks(tasksData);
      setIsLoading(false);
    } catch (err) {
      console.error('Error fetching tasks:', err);
      setError('Failed to load tasks. Please try again.');
      setIsLoading(false);
    }
  }

  // Filter tasks based on current filter
  const filteredTasks = tasks.filter(task => {
    if (filter === 'all') return true;
    return task.status === filter;
  });

  if (isLoading) {
    return <div className="loader">Loading tasks...</div>;
  }

  if (error) {
    return <div className="error-message">{error}</div>;
  }

  return (
    <div className="tasks-container">
      <div className="tasks-header">
        <h1>Tasks</h1>
        <div className="filters">
          <button 
            className={filter === 'all' ? 'active' : ''} 
            onClick={() => setFilter('all')}
          >
            All
          </button>
          <button 
            className={filter === 'open' ? 'active' : ''} 
            onClick={() => setFilter('open')}
          >
            Open
          </button>
          <button 
            className={filter === 'in_progress' ? 'active' : ''} 
            onClick={() => setFilter('in_progress')}
          >
            In Progress
          </button>
          <button 
            className={filter === 'completed' ? 'active' : ''} 
            onClick={() => setFilter('completed')}
          >
            Completed
          </button>
        </div>
      </div>

      <div className="tasks-list">
        {filteredTasks.map(task => (
          <div key={task.id} className="task-card">
            <h3>
              <Link to={`/tasks/${task.id}`}>{task.title}</Link>
            </h3>
            <p className="task-description">{task.description}</p>
            <div className="task-details">
              <span className={`status-badge ${task.status}`}>{task.status}</span>
              <span className="assigned-to">Assigned to: {task.assigned_to}</span>
            </div>
          </div>
        ))}
        
        {filteredTasks.length === 0 && (
          <div className="no-tasks">
            <p>No tasks found with the selected filter.</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default TasksList;
