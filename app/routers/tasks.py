from fastapi import APIRouter

router = APIRouter()

# Example route for task management
@router.get("/tasks", tags=["Tasks"])
async def get_tasks():
    return {"message": "List of tasks"}