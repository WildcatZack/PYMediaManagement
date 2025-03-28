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
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd PYMediaManagement
   ```

2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

5. Open the app in your browser:
   - Navigate to `http://127.0.0.1:8000`.

## Project Structure
```plaintext
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
```

## Next Steps
1. **Add a Router for Modular API Design**:
   - Create a `routers` directory and add a basic router for task management or file processing.

2. **Set Up the Database**:
   - Add SQLite integration using `SQLAlchemy` or `Tortoise ORM`.
   - Create a `database.py` file to manage the connection and schema.

3. **Implement Task Management**:
   - Add a route to create, view, and manage tasks.
   - Use a simple in-memory task list for now, and later integrate it with the database.

4. **Improve the Web UI**:
   - Add a navigation bar and a basic layout using Jinja2 templates.
   - Include CSS for styling.

5. **Add Configuration Support**:
   - Use a `.env` file to manage environment variables (e.g., database URL, Plex API key).

6. **Set Up Docker**:
   - Create a `Dockerfile` and `docker-compose.yml` for containerized deployment.

## Notes for Future Chatbots
- Use FastAPI for the backend and Jinja2 for the frontend.
- SQLite is the default database, but allow for external database configuration.
- Follow the project structure and add features incrementally.
- Use Docker for deployment (to be added later).

## License
This project is licensed under the MIT License.