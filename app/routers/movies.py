from fastapi import APIRouter, HTTPException
from app.database import database
from app.models import movies
from sqlalchemy import select
from pydantic import BaseModel

router = APIRouter()

# Pydantic model for creating a movie
class MovieCreate(BaseModel):
    title: str
    file_path: str

# Pydantic model for updating a movie
class MovieUpdate(BaseModel):
    title: str = None
    file_path: str = None

# Create a new movie
@router.post("/movies", tags=["Movies"])
async def create_movie(movie: MovieCreate):
    query = movies.insert().values(
        title=movie.title,
        file_path=movie.file_path,
    )
    movie_id = await database.execute(query)
    return {"id": movie_id, "title": movie.title, "file_path": movie.file_path}

# Get all movies
@router.get("/movies", tags=["Movies"])
async def get_movies():
    query = select(movies)
    results = await database.fetch_all(query)
    return results

# Get a single movie by ID
@router.get("/movies/{movie_id}", tags=["Movies"])
async def get_movie(movie_id: int):
    query = select(movies).where(movies.c.id == movie_id)
    movie = await database.fetch_one(query)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

# Update a movie
@router.put("/movies/{movie_id}", tags=["Movies"])
async def update_movie(movie_id: int, movie_update: MovieUpdate):
    query = select(movies).where(movies.c.id == movie_id)
    movie = await database.fetch_one(query)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    update_query = movies.update().where(movies.c.id == movie_id).values(
        title=movie_update.title if movie_update.title is not None else movie["title"],
        file_path=movie_update.file_path if movie_update.file_path is not None else movie["file_path"],
    )
    await database.execute(update_query)

    updated_movie = await database.fetch_one(query)
    return updated_movie

# Delete a movie
@router.delete("/movies/{movie_id}", tags=["Movies"])
async def delete_movie(movie_id: int):
    query = select(movies).where(movies.c.id == movie_id)
    movie = await database.fetch_one(query)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    delete_query = movies.delete().where(movies.c.id == movie_id)
    await database.execute(delete_query)
    return {"message": f"Movie with ID {movie_id} has been deleted"}