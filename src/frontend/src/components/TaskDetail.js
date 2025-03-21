import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { API } from 'aws-amplify';

const TaskDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [task, setTask] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isEditing, setIsEditing] = useState(false);
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    status: '',
    assigned_to: ''
  });

  useEffect(() => {
    fetchTask();
  }, [id]);

  async function fetchTask() {
    try {
      setIsLoading(true);
      const taskData = await API.get('api', `/tasks/${id}`);
      setTask(taskData);
      setFormData({
        title: taskData.title,
        description: taskData.description,
        status: taskData.status,
        assigned_to: taskData.assigned_to
      });
      setIsLoading(false);
    } catch (err) {
      console.error('Error fetching task:', err);
      setError('Failed to load task details. Please try again.');
      setIsLoading(false);
    }
  }

  async function handleUpdateTask(e) {
    e.preventDefault();
    try {
      const updatedTask = await API.put('api', `/tasks/${id}`, {
        body: formData
      });
      setTask(updatedTask);
      setIsEditing(false);
    } catch (err) {
      console.error('Error updating task:', err);
      setError('Failed to update task. Please try again.');
    }
  }

  function handleChange(e) {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  }

  if (isLoading) {
    return <div className="loader">Loading task details...</div>;
  }

  if (error) {
    return <div className="error-message">{error}</div>;
  }

  if (!task) {
    return <div className="not-found">Task not found</div>;
  }

  return (
    <div className="task-detail-container">
      <div className="task-detail-header">
        <button className="back-button" onClick={() => navigate('/tasks')}>
          &larr; Back to Tasks
        </button>
        <div className="task-actions">
          {isEditing ? (
            <button className="cancel-button" onClick={() => setIsEditing(false)}>
              Cancel
            </button>
          ) : (
            <button className="edit-button" onClick={() => setIsEditing(true)}>
              Edit Task
            </button>
          )}
        </div>
      </div>

      {isEditing ? (
        <form className="task-edit-form" onSubmit={handleUpdateTask}>
          <div className="form-group">
            <label htmlFor="title">Title</label>
            <input
              type="text"
              id="title"
              name="title"
              value={formData.title}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="description">Description</label>
            <textarea
              id="description"
              name="description"
              value={formData.description}
              onChange={handleChange}
              rows="4"
            />
          </div>

          <div className="form-group">
            <label htmlFor="status">Status</label>
            <select
              id="status"
              name="status"
              value={formData.status}
              onChange={handleChange}
              required
            >
              <option value="open">Open</option>
              <option value="in_progress">In Progress</option>
              <option value="completed">Completed</option>
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="assigned_to">Assigned To</label>
            <input
              type="email"
              id="assigned_to"
              name="assigned_to"
              value={formData.assigned_to}
              onChange={handleChange}
            />
          </div>

          <div className="form-actions">
            <button type="submit" className="save-button">Save Changes</button>
          </div>
        </form>
      ) : (
        <div className="task-detail-content">
          <h1 className="task-title">{task.title}</h1>
          <div className="task-meta">
            <span className={`status-badge ${task.status}`}>{task.status}</span>
            <span className="assigned-to">Assigned to: {task.assigned_to}</span>
          </div>
          <div className="task-description">
            <h3>Description</h3>
            <p>{task.description || 'No description provided.'}</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default TaskDetail;
