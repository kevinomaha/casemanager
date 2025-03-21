# Workflow Manager Architecture Model

## System Architecture

```
+-------------------+    +-------------------+    +-------------------+
|                   |    |                   |    |                   |
|  Web Application  |<-->|  API Services     |<-->|  Database Layer   |
|  (Flask)          |    |  (Flask-RESTful)  |    |  (PostgreSQL)     |
|                   |    |                   |    |                   |
+-------------------+    +-------------------+    +-------------------+
        ^                        ^                        ^
        |                        |                        |
        v                        v                        v
+-------------------+    +-------------------+    +-------------------+
|                   |    |                   |    |                   |
|  Authentication   |    |  Notification     |    |  AWS Services     |
|  Services         |    |  Services         |    |  (S3, SNS, etc.)  |
|                   |    |                   |    |                   |
+-------------------+    +-------------------+    +-------------------+
```

## Component Descriptions

### Web Application Layer
- Provides user interface for creating, updating, and managing tasks
- Implements responsive design for desktop and mobile access
- Renders task dashboards, forms, and notification views

### API Services Layer
- RESTful API endpoints for task CRUD operations
- Business logic for workflow management
- Task status validation and transitions
- User permissions and access control

### Database Layer
- Stores task data, user information, and system configurations
- Maintains relationships between tasks, cases, and users
- Tracks task history and audit trail

### Authentication Services
- User authentication and session management
- Role-based access control
- JWT token validation

### Notification Services
- Real-time notifications for task status changes
- Email, SMS, and in-app notifications
- Notification preferences and subscriptions

### AWS Services Integration
- S3 for document storage
- SNS for notification delivery
- Lambda for serverless event processing
- CloudWatch for monitoring and logging

## Data Model

### Task
- id: UUID (Primary Key)
- title: String
- description: Text
- status: Enum (New, In Progress, On Hold, Completed, Cancelled)
- priority: Enum (Low, Medium, High, Critical)
- due_date: DateTime
- assigned_to: User ID (Foreign Key)
- created_by: User ID (Foreign Key)
- created_at: DateTime
- updated_at: DateTime
- case_id: UUID (Foreign Key)
- tags: Array of Strings

### User
- id: UUID (Primary Key)
- username: String
- email: String
- full_name: String
- role: Enum (Admin, Manager, Agent, Viewer)
- department: String
- created_at: DateTime
- last_login: DateTime

### Notification
- id: UUID (Primary Key)
- user_id: UUID (Foreign Key)
- content: Text
- type: Enum (Task Assignment, Status Change, Due Date, Comment)
- read: Boolean
- created_at: DateTime
- related_task_id: UUID (Foreign Key)

### TaskHistory
- id: UUID (Primary Key)
- task_id: UUID (Foreign Key)
- changed_by: UUID (Foreign Key)
- change_type: Enum (Creation, Status Change, Assignment, Edit)
- old_value: JSON
- new_value: JSON
- changed_at: DateTime

## API Endpoints

### Tasks
- GET /api/tasks - List all tasks
- GET /api/tasks/{id} - Get task details
- POST /api/tasks - Create new task
- PUT /api/tasks/{id} - Update task
- DELETE /api/tasks/{id} - Delete task
- PATCH /api/tasks/{id}/status - Update task status

### Users
- GET /api/users - List all users
- GET /api/users/{id} - Get user details
- POST /api/users - Create new user
- PUT /api/users/{id} - Update user

### Notifications
- GET /api/notifications - Get user notifications
- PATCH /api/notifications/{id}/read - Mark notification as read
- POST /api/notifications/settings - Update notification preferences
