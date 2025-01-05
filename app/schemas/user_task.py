from pydantic import BaseModel
from enum import Enum
from datetime import date

class TaskStatus(Enum):
    PENDING = "Pending"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"

class TaskBase(BaseModel):
    todolist: str
    date : date
    status: TaskStatus = TaskStatus.PENDING


# task request
class TaskCreate(TaskBase):
    pass  

# task response
class Task(TaskBase):
    task_id: int
    reference_id: str
    todolist: str
    date: date
    status: str

    class Config:
        from_attributes = True

class TaskStatusCount(BaseModel):
    pending_count: int
    in_progress_count: int
    completed_count: int

    class Config:
        orm_mode = True