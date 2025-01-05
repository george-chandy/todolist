from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import APIKeyHeader, OAuth2PasswordBearer
from sqlalchemy.orm import Session
# from todolist import app
from app.database import database
from app.schemas import user_task
from app.services import user_service
from app.services.task_service import create_task,get_tasks_by_reference_id,get_id_to_delete,get_id_to_update
from app.routes.route_auth import decode_jwt,oauth2_scheme

# from app.services.auth import get_current_user


taskrouter = APIRouter(
    tags=["tasks"],
)


router = APIRouter()
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
API_KEY_NAME = "Authorization"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)


@router.post("/tasks/", response_model=user_task.Task)
async def add_task(
    task: user_task.TaskCreate,
    db: Session = Depends(database.get_db),
    token: str = Depends(oauth2_scheme),
):
    # Decode the token and extract Auth0 user_id
    user_info = decode_jwt(token)
    reference_id = user_info["sub"]  # Auth0 user_id
    
    # Create the task in the database
    new_task = create_task(db, reference_id=reference_id, todolist=task.todolist,status=task.status)
    return new_task


@router.get("/tasks/",response_model=user_task.Task)
async def get_task(
    skip:int=0,
    limit:int=10,
    db: Session=Depends(database.get_db),
    token: str = Depends(oauth2_scheme),
):
    user_info = decode_jwt(token)
    reference_id = user_info["sub"] 

    tasks_to_get= get_tasks_by_reference_id (db,reference_id,skip,limit)
    return tasks_to_get

   
@router.put("/tasks/{task_id}", response_model=user_task.Task)
async def update_task(
    task_id: int,
    task: user_task.TaskCreate,
    db: Session = Depends(database.get_db),
    token: str = Depends(oauth2_scheme),
):
    user_info = decode_jwt(token)
    reference_id = user_info["sub"] 

    task_to_update=get_id_to_update(db,reference_id,todolist=task.todolist,status=task.status)

    if not task_to_update:
        raise HTTPException(status_code=404, detail="Task not found")

    # if not updated_task:
    #     raise HTTPException(status_code=400, detail="Failed to update task")
    
    # if task_to_update.reference_id != reference_id:
    #     raise HTTPException(status_code=403, detail="Not authorized to update this task")
    
    updated_task = update_task(db, task_id, task.todolist, task.status)
    return updated_task


@router.delete("/tasks/{task_id}", response_model=user_task.Task)
async def delete_task(
    task_id: int,
    task: user_task.TaskCreate,
    db: Session = Depends(database.get_db),
    token: str = Depends(oauth2_scheme),
):
    user_info = decode_jwt(token)
    reference_id = user_info["sub"] 
 
    task_to_delete = get_id_to_delete(db,reference_id,)

    if not task_to_delete:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # if task_to_delete.reference_id != reference_id:
    #     raise HTTPException(status_code=403, detail="Not authorized to delete this task")

    deleted_task = delete_task(db,task_id)
    return deleted_task






'''def get_current_user(api_key: str = Security(api_key_header)):
    if api_key and api_key.startswith("Bearer "):
        api_key = api_key[7:]  # Remove "Bearer " prefix
    return api_key

@router.post("/tasks/", response_model=user_task.Task)
def create_task(task: user_task.TaskCreate, db: Session = Depends(database.get_db), token=Depends(get_current_user)):
    # return task_service.create_task(db, task, user["sub"])
    print(token)
    pass

@router.get("/tasks/", response_model=list[user_task.Task])
def get_tasks(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db), user=Depends(get_current_user)):
    return task_service.get_tasks(db, user["sub"], skip, limit)

@router.put("/tasks/{task_id}", response_model=user_task.Task)
def update_task(task_id: int, task: user_task.TaskCreate, db: Session = Depends(database.get_db), user=Depends(get_current_user)):
    return task_service.update_task(db, task_id, task.dict(), user["sub"])

@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(database.get_db), user=Depends(get_current_user)):
    return task_service.delete_task(db, task_id, user["sub"])
'''


# @app.get("/tasks/", response_model=list[user_task.Task])
# async def read_tasks(
#     skip: int = 0,
#     limit: int = 100,
#     db: AsyncSession = Depends(database.get_db),
# ):
#     tasks = await todoservices.get_tasks(db, skip=skip, limit=limit)
#     return tasks


# @app.get("/tasks/{task_id}", response_model=user_task.Task)
# async def read_task(task_id: int, db: AsyncSession = Depends(database.get_db)):
#     db_task = await todoservices.get_task(db, task_id=task_id)
#     if db_task is None:
#         raise HTTPException(status_code=404, detail="Task not found")
#     return db_task


# @app.post("/tasks/", response_model=user_task.Task)
# async def create_task(
#     task: user_task.TaskCreate, db: AsyncSession = Depends(database.get_db)
# ):
#     return await todoservices.create_task(db=db, task=task)


# @app.put("/tasks/{task_id}", response_model=user_task.Task)
# async def update_task(
#     task_id: int, task: user_task.Task, db: AsyncSession = Depends(database.get_db)
# ):
#     db_task = await todoservices.update_task(db, task_id, task)
#     if db_task is None:
#         raise HTTPException(status_code=404, detail="Task not found")
#     return db_task


# @app.delete("/tasks/{task_id}", response_model=user_task.Task)
# async def delete_task(task_id: int, db: AsyncSession = Depends(database.get_db)):
#     db_task = await todoservices.delete_task(db, task_id)
#     if db_task is None:
#         raise HTTPException(status_code=404, detail="Task not found")
#     return db_task







