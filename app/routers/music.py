from fastapi import APIRouter, HTTPException
from app.database import database
from app.models import music
from sqlalchemy import select
from pydantic import BaseModel

router = APIRouter()

# Pydantic model for creating a music entry
class MusicCreate(BaseModel):
    title: str
    artist: str = None
    album: str = None
    file_path: str

# Pydantic model for updating a music entry
class MusicUpdate(BaseModel):
    title: str = None
    artist: str = None
    album: str = None
    file_path: str = None

# Create a new music entry
@router.post("/music", tags=["Music"])
async def create_music(music_entry: MusicCreate):
    query = music.insert().values(
        title=music_entry.title,
        artist=music_entry.artist,
        album=music_entry.album,
        file_path=music_entry.file_path,
    )
    music_id = await database.execute(query)
    return {
        "id": music_id,
        "title": music_entry.title,
        "artist": music_entry.artist,
        "album": music_entry.album,
        "file_path": music_entry.file_path,
    }

# Get all music entries
@router.get("/music", tags=["Music"])
async def get_music():
    query = select(music)
    results = await database.fetch_all(query)
    return results

# Get a single music entry by ID
@router.get("/music/{music_id}", tags=["Music"])
async def get_music_entry(music_id: int):
    query = select(music).where(music.c.id == music_id)
    music_entry = await database.fetch_one(query)
    if not music_entry:
        raise HTTPException(status_code=404, detail="Music entry not found")
    return music_entry

# Update a music entry
@router.put("/music/{music_id}", tags=["Music"])
async def update_music(music_id: int, music_update: MusicUpdate):
    query = select(music).where(music.c.id == music_id)
    music_entry = await database.fetch_one(query)
    if not music_entry:
        raise HTTPException(status_code=404, detail="Music entry not found")

    update_query = music.update().where(music.c.id == music_id).values(
        title=music_update.title if music_update.title is not None else music_entry["title"],
        artist=music_update.artist if music_update.artist is not None else music_entry["artist"],
        album=music_update.album if music_update.album is not None else music_entry["album"],
        file_path=music_update.file_path if music_update.file_path is not None else music_entry["file_path"],
    )
    await database.execute(update_query)

    updated_music_entry = await database.fetch_one(query)
    return updated_music_entry

# Delete a music entry
@router.delete("/music/{music_id}", tags=["Music"])
async def delete_music(music_id: int):
    query = select(music).where(music.c.id == music_id)
    music_entry = await database.fetch_one(query)
    if not music_entry:
        raise HTTPException(status_code=404, detail="Music entry not found")

    delete_query = music.delete().where(music.c.id == music_id)
    await database.execute(delete_query)
    return {"message": f"Music entry with ID {music_id} has been deleted"}