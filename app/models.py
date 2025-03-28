from sqlalchemy import Table, Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.database import metadata

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