# from fastapi import APIRouter, FastAPI, Depends, HTTPException
# from sqlalchemy.ext.asyncio import AsyncSession

# from app.services import user_service
# from app.models import user_task_models
# from app.schemas import user_schema
# from app.database import database


# userrouter = APIRouter(
#     tags=["users"],
# )

# router = APIRouter()

# # @router.post("/users/", response_model=user_schema.User)
# # async def create_user(user: user_schema.UserCreate, db: AsyncSession = Depends(database.get_db)):
# #     db_user = await user_service.get_user_by_username(db, name=user.username)
# #     if db_user:
# #         raise HTTPException(status_code=400, detail="User already registered")
# #     return await user_service.create_user(db=db, user=user)

# @router.post("/users/", response_model=user_schema.User)
# def create_user(user: user_schema.UserCreate, db: AsyncSession = Depends(database.get_db)):
#     # db_user = user_service.get_user_by_username(db, username=user.username)
#     # if db_user:
#     #     raise HTTPException(status_code=400, detail="User already registered")

#     # # Create a new user
#     return user_service.create_new_user(db=db, user_data=user)

# @router.get("/users/{user_id}", response_model=user_schema.User)
# async def read_user(user_id: int, db: AsyncSession = Depends(database.get_db)):
#     db_user = await user_service.get_user_by_id(db, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user
