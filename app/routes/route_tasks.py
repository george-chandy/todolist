import token
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import APIKeyHeader
from sqlalchemy import func
from sqlalchemy.orm import Session
# from todolist import app
from app.database import database
from app.schemas import user_task
from app.services import user_service
from app.services.task_service import create_task, get_pending_tasks_count_for_user,get_tasks_by_reference_id,get_id_to_delete,get_id_to_update, perform_task_update
from app.routes.route_auth import decode_jwt,oauth2_scheme

# from app.services.auth import get_current_user


taskrouter = APIRouter(
    tags=["tasks"],
)


router = APIRouter()
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
API_KEY_NAME = "Authorization"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, "your_auth0_secret", algorithms=["RS256"])
        auth0_sub = payload.get("sub")  # Use "email" if preferred
        if not auth0_sub:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication token",
            )
        return auth0_sub
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )


'''

@router.post("/tasks/", response_model=user_task.TaskCreate)
async def add_task(
    task: user_task.TaskCreate,
    db: Session = Depends(database.get_db),
    token: str = Depends(oauth2_scheme),
):
    # Decode the token and extract Auth0 user_id
    user_info = decode_jwt(token)
    reference_id = user_info["sub"]  # Auth0 user_id
    
    # Create the task in the database
    new_task = create_task(db, todolist=task.todolist,status=task.status)
    return new_task
'''
@router.post("/tasks/", response_model=user_task.TaskCreate)
def create_task(
    task:user_task.TaskCreate,
    auth0_sub: str = Depends(get_current_user),  # Extract Auth0 subject (sub)
    db: Session = Depends(database.get_db)          # Connect to DB
):
    # Step 1: Query the `users` table to get the user UUID
    user = db.execute(
        "SELECT uuid FROM public.users WHERE auth0_sub = :auth0_sub",
        {"auth0_sub": auth0_sub}
    ).fetchone()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user_uuid = user.uuid

    # Step 2: Dynamically set the schema using the user's UUID
    schema_name = f"user_{user_uuid}"  # Construct the schema name
    db.execute(f'SET search_path TO "{schema_name}"')

    # Step 3: Insert the task into the user's `tasks` table
    new_task = create_task(db, todolist=task.todolist,status=task.status)
    return new_task

    return {"message": f"Task created successfully in schema '{schema_name}'"}


@router.get("/tasks/",response_model=list[user_task.Task])
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

# @router.get("/task_count/", response_model=user_task.TaskStatusCount)
# async def get_task_count(
#     db: Session = Depends(database.get_db),
#     token: str = Depends(oauth2_scheme)

# ):
#     user_info = decode_jwt(token)
#     reference_id = user_info["sub"] 

#     task_counts = task_count_of_user(db, reference_id)
#     return user_task.TaskStatusCount(
#         pending_count=task_counts['Pending'],
#         in_progress_count=task_counts['In Progress'],
#         completed_count=task_counts['Completed']
#     )
    
   
@router.put("/tasks/{task_id}", response_model=user_task.TaskBase)
async def update_task(
    task_id: int,
    task: user_task.TaskCreate,
    db: Session = Depends(database.get_db),
    token: str = Depends(oauth2_scheme),
):
    user_info = decode_jwt(token)
    reference_id = user_info["sub"] 

    task_to_update= get_id_to_update(db,task_id,todolist=task.todolist,status=task.status)

    if not task_to_update:
        raise HTTPException(status_code=404, detail="Task not found")

    # if not updated_task:
        # raise HTTPException(status_code=400, detail="Failed to update task")
    
    if task_to_update.reference_id != reference_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this task")
    
    # updated_task = await perform_task_update(db, task_id, task.todolist, task.status)
    return task_to_update


@router.delete("/tasks/{task_id}", response_model=user_task.Task)
async def delete_task(
    task_id: int,
    task: user_task.TaskCreate,
    db: Session = Depends(database.get_db),
    token: str = Depends(oauth2_scheme),
):
    user_info = decode_jwt(token)
    reference_id = user_info["sub"] 
 
    task_to_delete = get_id_to_delete(db,task_id,)

    if not task_to_delete:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # if task_to_delete.reference_id != reference_id:
    #     raise HTTPException(status_code=403, detail="Not authorized to delete this task")

    # deleted_task =  delete_task(db,task_id)
    return task_to_delete





@router.get("/tasks/pending_tasks_count/", response_model=user_task.PendingTaskCount)
async def get_pending_tasks(
    db: Session = Depends(database.get_db),
    token: str = Depends(oauth2_scheme)
):
    user_info = decode_jwt(token)
    reference_id = user_info["sub"]

    # Call the function without passing 'pending_count' as a keyword argument
    pending_count = get_pending_tasks_count_for_user(db, reference_id)

    # Return the result
    return {"pending_count": pending_count}






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







