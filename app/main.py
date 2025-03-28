from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from app.routers import tasks  # Import the tasks router
from app.database import database  # Import the database connection

# Initialize the FastAPI app
app = FastAPI()

# Set up Jinja2 templates
templates = Jinja2Templates(directory="app/templates")

# Include the tasks router
app.include_router(tasks.router, prefix="/api", tags=["Tasks"])

# Define a basic route
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "message": "Welcome to PYMediaManagement!"})

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