from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
import boto3
import json
import os
from src.utils.cognito_verify import verify_cognito_token

tasks_blueprint = Blueprint('tasks', __name__)

# Sample tasks data (in a real app, this would be stored in a database)
tasks = [
    {
        'id': 1,
        'title': 'Review case documents',
        'description': 'Review all case documents for completeness',
        'status': 'open',
        'assigned_to': 'user@example.com'
    },
    {
        'id': 2,
        'title': 'Schedule client meeting',
        'description': 'Set up initial consultation with client',
        'status': 'in_progress',
        'assigned_to': 'manager@example.com'
    }
]

@tasks_blueprint.route('/', methods=['GET'])
def get_tasks():
    """
    Get all tasks
    In production, this endpoint would be protected with JWT verification
    """
    # Get the token from Authorization header
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith('Bearer '):
        token = auth_header.split('Bearer ')[1]
        # Optional: Verify the token with Cognito
        # This step is not required for this demo but would be in production
        # user_info = verify_cognito_token(token)
    
    # Return all tasks for now - in a real app you would filter by user/permissions
    return jsonify(tasks)

@tasks_blueprint.route('/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """Get a specific task by ID"""
    task = next((task for task in tasks if task['id'] == task_id), None)
    
    if not task:
        return jsonify({'error': 'Task not found'}), 404
        
    return jsonify(task)

@tasks_blueprint.route('/', methods=['POST'])
def create_task():
    """Create a new task"""
    data = request.get_json()
    
    if not data or not data.get('title'):
        return jsonify({'error': 'Title is required'}), 400
    
    # Get the current user's email from the token (if available)
    user_email = 'default@example.com'  # Default value
    
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith('Bearer '):
        token = auth_header.split('Bearer ')[1]
        # In production, you would verify the token and extract user info
        # user_info = verify_cognito_token(token)
        # user_email = user_info.get('email', user_email)
    
    # Create a new task
    new_task = {
        'id': max(task['id'] for task in tasks) + 1 if tasks else 1,
        'title': data.get('title'),
        'description': data.get('description', ''),
        'status': data.get('status', 'open'),
        'assigned_to': data.get('assigned_to', user_email)
    }
    
    tasks.append(new_task)
    
    return jsonify(new_task), 201

@tasks_blueprint.route('/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Update an existing task"""
    task = next((task for task in tasks if task['id'] == task_id), None)
    
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Update task fields
    if 'title' in data:
        task['title'] = data['title']
    if 'description' in data:
        task['description'] = data['description']
    if 'status' in data:
        task['status'] = data['status']
    if 'assigned_to' in data:
        task['assigned_to'] = data['assigned_to']
    
    return jsonify(task)

@tasks_blueprint.route('/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task"""
    task = next((task for task in tasks if task['id'] == task_id), None)
    
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    tasks.remove(task)
    
    return jsonify({'message': 'Task deleted successfully'})
