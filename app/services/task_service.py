from fastapi import HTTPException
# from models import user_task_models
# from schemas import user_task
from sqlalchemy import case, func
from sqlalchemy.orm import Session
from app.models.user_task_models import Tasks
from app.schemas import user_task
from sqlalchemy.orm import Session
from datetime import date
from sqlalchemy.sql import case





def create_task(session: Session, todolist: str, status:str):
    new_task = Tasks(
          # Auth0 user ID
        date=date.today(),
        todolist=todolist,
        status=status  
    )
    session.add(new_task)
    session.commit()
    return new_task


def get_tasks_by_reference_id(db: Session, reference_id: str,skip:int,limit:int):
    tasks= db.query(Tasks).filter(Tasks.reference_id==reference_id).offset(skip).limit(limit).all()
    return tasks
  
def get_id_to_update(session: Session, task_id: int, todolist: str, status: str):
    task = session.query(Tasks).filter(Tasks.task_id == task_id).first()
    # if not task:
    #     return None
    task.todolist = todolist
    task.status = status
    session.commit()
    return task


def get_id_to_delete(session: Session, task_id: int):
    task = session.query(Tasks).filter(Tasks.task_id == task_id).first()
    if not task:
        return None
    session.delete(task)
    session.commit()
    return task



def get_pending_tasks_count_for_user(db: Session, reference_id: int) -> int:
    pending_count = (
        db.query(func.count(Tasks.task_id))
        .filter(Tasks.reference_id == reference_id, Tasks.status == 'Pending')
        .scalar()  # Returns the count as a single value
    )

    return pending_count or 0  # Default to 0 if no tasks exist


async def perform_task_update(db: Session, task_id: int, todolist: str, status: str):
    # Logic to update the task in the database
    task = db.query(user_task.Task).filter(user_task.Task.id == task_id).first()
    if task:
        task.todolist = todolist
        task.status = status
        db.commit()
        db.refresh(task)
        return task
    return None












# def task_count_of_user (db: Session, reference_id: int):
#     result = (
#         db.query(
#             case([(Tasks.status == 'Pending', 'Pending')], else_='').label('status'),
#             func.count(case([(Tasks.status == 'Pending', 1)], else_=None)).label('count')
#         )
#         .filter(Tasks.reference_id == reference_id)  # Filter by the specific user_id
#         .group_by('status')  # Group by status (Pending, In Progress, Completed)
#         .all()  # Get all results
#     )
    
#     # Convert the result into a dictionary with status as the key and count as the value
#     task_counts = {row.status: row.count for row in result}
    
#     # Provide a default value of 0 for statuses that don't exist in the result
#     task_counts.setdefault('Pending', 0)
#     task_counts.setdefault('In Progress', 0)
#     task_counts.setdefault('Completed', 0)
    
#     return task_counts



# def create_task(db: Session, task_data: user_task.TaskCreate, user_id: int):
#     new_task = Tasks(
#         title=task_data.title,
#         date=task_data.date,
#         status=task_data.status,
#         user_id=user_id
#     )
#     db.add(new_task)
#     db.commit()
#     db.refresh(new_task)
#     return new_task


# def get_tasks(db: Session, user_id: int, skip: int, limit: int):
#     return db.query(Tasks).filter(Tasks.task_user_id == user_id).offset(skip).limit(limit).all()

# def update_task(db: Session, task_id: int, task_data: dict, user_id: int):
#     task = db.query(Tasks).filter(Tasks.task_id == task_id, Tasks.task_user_id == user_id).first()
#     if not task:
#         raise HTTPException(status_code=404, detail="Task not found")
#     for key, value in task_data.items():
#         setattr(task, key, value)
#     db.commit()
#     db.refresh(task)
#     return task

# def delete_task(db: Session, task_id: int, user_id: int):
#     task = db.query(Tasks).filter(Tasks.task_id == task_id, Tasks.task_user_id == user_id).first()
#     if not task:
#         raise HTTPException(status_code=404, detail="Task not found")
#     db.delete(task)
#     db.commit()
#     return {"detail": "Task deleted"}




