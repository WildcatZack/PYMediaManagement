from sqlalchemy import Table, Column, Integer, String, Boolean, DateTime, MetaData
from sqlalchemy.sql import func
from app.database import metadata
from pydantic import BaseModel
from fastapi import APIRouter

router = APIRouter()

# Define the Task model
tasks = Table(
    "tasks",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("title", String, nullable=False),
    Column("description", String, nullable=True),
    Column("completed", Boolean, default=False),
    Column("created_at", DateTime, server_default=func.now()),
    Column("updated_at", DateTime, server_default=func.now(), onupdate=func.now()),
)

# Shows Table
shows = Table(
    "shows",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("title", String, nullable=False),
    Column("file_path", String, nullable=False),
    Column("season", Integer, nullable=True),
    Column("episode", Integer, nullable=True),
    Column("created_at", DateTime, server_default=func.now()),
)

# Movies Table
movies = Table(
    "movies",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("title", String, nullable=False),
    Column("file_path", String, nullable=False),
    Column("created_at", DateTime, server_default=func.now()),
)

# Music Table
music = Table(
    "music",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("title", String, nullable=False),
    Column("artist", String, nullable=True),
    Column("album", String, nullable=True),
    Column("file_path", String, nullable=False),
    Column("created_at", DateTime, server_default=func.now()),
)

