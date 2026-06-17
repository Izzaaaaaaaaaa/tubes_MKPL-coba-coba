from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, description="Judul task")
    description: str | None = Field(
        default=None, max_length=500, description="Deskripsi task"
    )


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    is_completed: bool | None = None


class Task(TaskBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_completed: bool
    created_at: datetime
