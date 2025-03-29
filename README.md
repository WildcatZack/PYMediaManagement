# PYMediaManagement

## Overview
PYMediaManagement is a media management tool designed for users hosting a Plex Media Server. It provides a web-based interface to manage tasks, process media files, and integrate with Plex.

## Features
- Task management for media processing
- File matching and renaming
- File conversion and moving
- Plex Media Server integration
- Web-based UI using Jinja2 templates

## Getting Started

### Prerequisites
- Python 3.10+
- Visual Studio Code Insiders
- iTerm2 (optional, for terminal commands)
- macOS Sequoia

### Installation
1. Clone the repository: `git clone <repository-url> && cd PYMediaManagement`
2. Create a virtual environment: `python3 -m venv venv && source venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Run the application: `uvicorn app.main:app --reload`
5. Open the app in your browser: Navigate to `http://127.0.0.1:8000`

## Project Structure
PYMediaManagement
├── app
│   ├── __init__.py
│   ├── main.py               # Entry point for the FastAPI app
│   ├── models.py             # Pydantic models and database schemas
│   ├── routers               # API routes
│   │   ├── __init__.py
│   │   └── ...               # Additional route files
│   ├── services              # Business logic and helper functions
│   │   ├── __init__.py
│   │   └── ...               # Additional service files
│   ├── templates             # Jinja2 templates for the web UI
│   ├── static                # Static files (CSS, JS, images)
│   └── database.py           # Database connection and setup
├── tests                     # Unit and integration tests
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation
├── .env                      # Environment variables

## Implementation Details

### Database Setup
- The application uses **SQLite** as the default database, with support for other SQL databases via SQLAlchemy.
- The database connection is managed using `databases` for async support.
- The `Task` model is defined with the following fields:
  - `id`: Primary key (integer).
  - `title`: Task title (string, required).
  - `description`: Task description (string, optional).
  - `completed`: Task completion status (boolean, default: `False`).
  - `created_at`: Timestamp for when the task was created.
  - `updated_at`: Timestamp for when the task was last updated.

### CRUD Operations for Task Management
The following endpoints are available for managing tasks:

1. **Create a Task**  
   - **Endpoint**: `POST /api/tasks`  
   - **Request Body**:
     ```json
     {
       "title": "My Task",
       "description": "This is a test task"
     }
     ```
   - **Response**:
     ```json
     {
       "id": 1,
       "title": "My Task",
       "description": "This is a test task",
       "completed": false
     }
     ```

2. **Get All Tasks**  
   - **Endpoint**: `GET /api/tasks`  
   - **Response**:
     ```json
     [
       {
         "id": 1,
         "title": "My Task",
         "description": "This is a test task",
         "completed": false,
         "created_at": "2025-03-28T12:00:00",
         "updated_at": "2025-03-28T12:00:00"
       }
     ]
     ```

3. **Get a Single Task by ID**  
   - **Endpoint**: `GET /api/tasks/{task_id}`  
   - **Response** (if the task exists):
     ```json
     {
       "id": 1,
       "title": "My Task",
       "description": "This is a test task",
       "completed": false,
       "created_at": "2025-03-28T12:00:00",
       "updated_at": "2025-03-28T12:00:00"
     }
     ```
   - **Response** (if the task does not exist):
     ```json
     {
       "detail": "Task not found"
     }
     ```

4. **Update a Task**  
   - **Endpoint**: `PUT /api/tasks/{task_id}`  
   - **Request Body**:
     ```json
     {
       "title": "Updated Task",
       "description": "This task has been updated",
       "completed": true
     }
     ```
   - **Response**:
     ```json
     {
       "id": 1,
       "title": "Updated Task",
       "description": "This task has been updated",
       "completed": true,
       "created_at": "2025-03-28T12:00:00",
       "updated_at": "2025-03-28T12:10:00"
     }
     ```

5. **Delete a Task**  
   - **Endpoint**: `DELETE /api/tasks/{task_id}`  
   - **Response**:
     ```json
     {
       "message": "Task with ID 1 has been deleted"
     }
     ```

### Database File
- The SQLite database file is named [pymediamanagement.db](http://_vscodecontentref_/2) and is located in the project root directory.
- Tables are automatically created on application startup.

## Next Steps
1. **Improve the Web UI**:
   - Add a navigation bar and a basic layout using Jinja2 templates.
   - Include CSS for styling.

2. **Add Configuration Support**:
   - Use a [.env](http://_vscodecontentref_/3) file to manage environment variables (e.g., database URL, Plex API key).

3. **Set Up Docker**:
   - Create a `Dockerfile` and `docker-compose.yml` for containerized deployment.

4. **Write Unit Tests**:
   - Add unit tests for the CRUD operations to ensure the application behaves as expected.

## Notes for Future Chatbots
- Use FastAPI for the backend and Jinja2 for the frontend.
- SQLite is the default database, but allow for external database configuration.
- Follow the project structure and add features incrementally.
- Use Docker for deployment (to be added later).
- **Automatically update the README** to reflect changes and progress in the project as new features or updates are implemented.
- Look for learning opportunities to teach the user FastAPI and asynchronous programming concepts as the project progresses.

## License
This project is licensed under the MIT License.