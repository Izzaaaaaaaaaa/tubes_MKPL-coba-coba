from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.database import get_db

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", response_model=schemas.Task, status_code=status.HTTP_201_CREATED)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)) -> models.Task:
    return crud.create_task(db=db, task=task)


@router.get("/", response_model=list[schemas.Task])
def read_tasks(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> list[models.Task]:
    return crud.get_tasks(db, skip=skip, limit=limit)


@router.get("/{task_id}", response_model=schemas.Task)
def read_task(task_id: int, db: Session = Depends(get_db)) -> models.Task:
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task tidak ditemukan"
        )
    return db_task


@router.patch("/{task_id}", response_model=schemas.Task)
def update_task(
    task_id: int, task_update: schemas.TaskUpdate, db: Session = Depends(get_db)
) -> models.Task:
    db_task = crud.update_task(db, task_id=task_id, task_update=task_update)
    if db_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task tidak ditemukan"
        )
    return db_task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)) -> None:
    success = crud.delete_task(db, task_id=task_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task tidak ditemukan"
        )
