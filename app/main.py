from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from app.routers import tasks, shows, movies, music  # Import the tasks, shows, movies, and music routers
from app.database import database  # Import the database connection
import requests
import yaml  # For parsing custom metadata files

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

# Add a route for shows
@app.get("/shows", response_class=HTMLResponse)
async def read_shows(request: Request):
    query = "SELECT * FROM shows"
    shows = await database.fetch_all(query=query)
    return templates.TemplateResponse("shows.html", {"request": request, "shows": shows})

# Add a route for creating a new show
@app.get("/shows/new", response_class=HTMLResponse)
async def new_show(request: Request):
    return templates.TemplateResponse("new_show.html", {"request": request})

# Add a route for editing an existing show
@app.get("/shows/{show_id}/edit", response_class=HTMLResponse)
async def edit_show(request: Request, show_id: int):
    query = "SELECT * FROM shows WHERE id = :id"
    show = await database.fetch_one(query=query, values={"id": show_id})
    if not show:
        raise HTTPException(status_code=404, detail="Show not found")
    return templates.TemplateResponse("edit_show.html", {"request": request, "show": show})

# Add a POST route to handle form submissions for creating a new show
@app.post("/shows/new", response_class=HTMLResponse)
async def search_and_add_show(
    source: str = Form(...),
    identifier: str = Form(...),
):
    # Search for the show based on the selected source
    if source == "tvdb":
        show_data = await search_tvdb(identifier)
    elif source == "custom":
        show_data = await search_custom_metadata(identifier)
    else:
        raise HTTPException(status_code=400, detail="Invalid source selected")

    # If no show data is found, return an error
    if not show_data:
        raise HTTPException(status_code=404, detail="Show not found")

    # Add the show to the database
    query = """
    INSERT INTO shows (title, file_path, season, episode)
    VALUES (:title, :file_path, :season, :episode)
    """
    await database.execute(query=query, values=show_data)

    return RedirectResponse(url="/shows", status_code=303)

# Add a POST route to handle form submissions for editing an existing show
@app.post("/shows/{show_id}/edit", response_class=HTMLResponse)
async def update_show(
    show_id: int,
    title: str = Form(...),
    file_path: str = Form(...),
    season: int = Form(None),
    episode: int = Form(None),
):
    query = """
    UPDATE shows
    SET title = :title, file_path = :file_path, season = :season, episode = :episode
    WHERE id = :id
    """
    await database.execute(query=query, values={"id": show_id, "title": title, "file_path": file_path, "season": season, "episode": episode})
    return RedirectResponse(url="/shows", status_code=303)

# Add a route for movies
@app.get("/movies", response_class=HTMLResponse)
async def read_movies(request: Request):
    query = "SELECT * FROM movies"
    movies = await database.fetch_all(query=query)
    return templates.TemplateResponse("movies.html", {"request": request, "movies": movies})

# Add a route for music
@app.get("/music", response_class=HTMLResponse)
async def read_music(request: Request):
    query = "SELECT * FROM music"
    music = await database.fetch_all(query=query)
    return templates.TemplateResponse("music.html", {"request": request, "music": music})

# Helper function to search TVDB
async def search_tvdb(identifier: str):
    # Replace with actual TVDB API logic
    response = requests.get(f"https://api.thetvdb.com/search?query={identifier}")
    if response.status_code == 200:
        data = response.json()
        return {
            "title": data["title"],
            "file_path": f"/tvdb/{data['id']}",
            "season": data.get("season", None),
            "episode": data.get("episode", None),
        }
    return None

# Helper function to search custom metadata
async def search_custom_metadata(file_path: str):
    # Replace with logic to parse a custom metadata file
    try:
        with open(file_path, "r") as file:
            data = yaml.safe_load(file)
            return {
                "title": data["title"],
                "file_path": file_path,
                "season": data.get("season", None),
                "episode": data.get("episode", None),
            }
    except Exception:
        return None