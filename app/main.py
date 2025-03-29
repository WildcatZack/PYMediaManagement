from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from app.routers import tasks, shows, movies, music  # Import the tasks, shows, movies, and music routers
from app.database import database  # Import the database connection

# Initialize the FastAPI app
app = FastAPI()

# Set up Jinja2 templates
templates = Jinja2Templates(directory="app/templates")

# Include the tasks router
app.include_router(tasks.router, prefix="/api", tags=["Tasks"])

# Include the shows router
app.include_router(shows.router, prefix="/api", tags=["Shows"])

# Include the movies router
app.include_router(movies.router, prefix="/api", tags=["Movies"])

# Include the music router
app.include_router(music.router, prefix="/api", tags=["Music"])

# Define the home route
@app.get("/", response_class=HTMLResponse)
async def read_home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

# Connect to the database on startup
@app.on_event("startup")
async def startup():
    await database.connect()

# Disconnect from the database on shutdown
@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/test-db")
async def test_db():
    try:
        # Run a simple query to check the connection
        query = "SELECT 1"
        result = await database.fetch_one(query=query)
        return {"status": "success", "result": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/tasks", response_class=HTMLResponse)
async def read_tasks(request: Request):
    # Fetch all tasks from the database
    query = "SELECT * FROM tasks"
    tasks = await database.fetch_all(query=query)
    return templates.TemplateResponse("tasks.html", {"request": request, "tasks": tasks})