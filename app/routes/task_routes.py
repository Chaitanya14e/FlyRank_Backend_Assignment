from fastapi import APIRouter, HTTPException, status

from app.schemas import TaskCreate, TaskUpdate
from app.services.task_service import TaskService
from app.repositories.postgres_task_repository import PostgresTaskRepository


router = APIRouter()


repository = PostgresTaskRepository()
service = TaskService(repository)


@router.get("/tasks")
def get_tasks():

    tasks = service.get_all_tasks()

    return {
        "data": tasks
    }


@router.get("/tasks/{task_id}")
def get_task(task_id: int):

    task = service.get_task(task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return {
        "data": task
    }


@router.post(
    "/tasks",
    status_code=status.HTTP_201_CREATED
)
def create_task(task: TaskCreate):

    try:

        new_task = service.create_task(task.title)

        return {
            "data": new_task
        }

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.put("/tasks/{task_id}")
def update_task(
    task_id: int,
    task: TaskUpdate
):

    try:

        updated_task = service.update_task(
            task_id,
            task.title,
            task.done
        )

        if updated_task is None:
            raise HTTPException(
                status_code=404,
                detail="Task not found"
            )

        return {
            "data": updated_task
        }

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_task(task_id: int):

    deleted = service.delete_task(task_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return