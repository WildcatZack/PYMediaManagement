from fastapi import APIRouter, HTTPException
from app.database import database
from app.models import tasks
from sqlalchemy import select
from pydantic import BaseModel

router = APIRouter()

# Pydantic model for task creation
class TaskCreate(BaseModel):
    title: str
    description: str = None

# Pydantic model for task updates
class TaskUpdate(BaseModel):
    title: str = None
    description: str = None
    completed: bool = None

# Create a new task
@router.post("/tasks", tags=["Tasks"])
async def create_task(task: TaskCreate):
    query = tasks.insert().values(title=task.title, description=task.description, completed=False)
    task_id = await database.execute(query)
    return {"id": task_id, "title": task.title, "description": task.description, "completed": False}

# Get all tasks
@router.get("/tasks", tags=["Tasks"])
async def get_tasks():
    query = select(tasks)  # Corrected: Pass tasks directly, not as a list
    results = await database.fetch_all(query)
    return results

# Get a single task by ID
@router.get("/tasks/{task_id}", tags=["Tasks"])
async def get_task(task_id: int):
    query = select(tasks).where(tasks.c.id == task_id)  # Corrected: Pass tasks directly, not as a list
    task = await database.fetch_one(query)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

# Update a task
@router.put("/tasks/{task_id}", tags=["Tasks"])
async def update_task(task_id: int, task_update: TaskUpdate):
    # Check if the task exists
    query = select(tasks).where(tasks.c.id == task_id)
    task = await database.fetch_one(query)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Update the task
    update_query = tasks.update().where(tasks.c.id == task_id).values(
        title=task_update.title if task_update.title is not None else task["title"],
        description=task_update.description if task_update.description is not None else task["description"],
        completed=task_update.completed if task_update.completed is not None else task["completed"],
    )
    await database.execute(update_query)

    # Fetch the updated task
    updated_task = await database.fetch_one(query)
    return updated_task

# Delete a task
@router.delete("/tasks/{task_id}", tags=["Tasks"])
async def delete_task(task_id: int):
    # Check if the task exists
    query = select(tasks).where(tasks.c.id == task_id)  # Corrected: Pass tasks directly, not as a list
    task = await database.fetch_one(query)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Delete the task
    delete_query = tasks.delete().where(tasks.c.id == task_id)
    await database.execute(delete_query)
    return {"message": f"Task with ID {task_id} has been deleted"}