from fastapi import APIRouter, HTTPException
from app.database import database
from app.models import shows
from sqlalchemy import select
from pydantic import BaseModel

router = APIRouter()

# Pydantic model for creating a show
class ShowCreate(BaseModel):
    title: str
    file_path: str
    season: int = None
    episode: int = None

# Pydantic model for updating a show
class ShowUpdate(BaseModel):
    title: str = None
    file_path: str = None
    season: int = None
    episode: int = None

# Create a new show
@router.post("/shows", tags=["Shows"])
async def create_show(show: ShowCreate):
    query = shows.insert().values(
        title=show.title,
        file_path=show.file_path,
        season=show.season,
        episode=show.episode,
    )
    show_id = await database.execute(query)
    return {"id": show_id, "title": show.title, "file_path": show.file_path, "season": show.season, "episode": show.episode}

# Get all shows
@router.get("/shows", tags=["Shows"])
async def get_shows():
    query = select(shows)
    results = await database.fetch_all(query)
    return results

# Get a single show by ID
@router.get("/shows/{show_id}", tags=["Shows"])
async def get_show(show_id: int):
    query = select(shows).where(shows.c.id == show_id)
    show = await database.fetch_one(query)
    if not show:
        raise HTTPException(status_code=404, detail="Show not found")
    return show

# Update a show
@router.put("/shows/{show_id}", tags=["Shows"])
async def update_show(show_id: int, show_update: ShowUpdate):
    query = select(shows).where(shows.c.id == show_id)
    show = await database.fetch_one(query)
    if not show:
        raise HTTPException(status_code=404, detail="Show not found")

    update_query = shows.update().where(shows.c.id == show_id).values(
        title=show_update.title if show_update.title is not None else show["title"],
        file_path=show_update.file_path if show_update.file_path is not None else show["file_path"],
        season=show_update.season if show_update.season is not None else show["season"],
        episode=show_update.episode if show_update.episode is not None else show["episode"],
    )
    await database.execute(update_query)

    updated_show = await database.fetch_one(query)
    return updated_show

# Delete a show
@router.delete("/shows/{show_id}", tags=["Shows"])
async def delete_show(show_id: int):
    query = select(shows).where(shows.c.id == show_id)
    show = await database.fetch_one(query)
    if not show:
        raise HTTPException(status_code=404, detail="Show not found")

    delete_query = shows.delete().where(shows.c.id == show_id)
    await database.execute(delete_query)
    return {"message": f"Show with ID {show_id} has been deleted"}