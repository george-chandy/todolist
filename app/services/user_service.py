# from sqlalchemy.orm import Session
# from app.models import user_task_models
# from app.schemas import user_schema
# from fastapi import HTTPException
# from app.models.user_task_models import Users

# def create_new_user(db: Session, user_data: user_schema.UserCreate):
#     # if db.query(Users).filter(Users.username == user_data.username).first():
#     #     raise HTTPException(status_code=400, detail="Username already exists")
#     new_user = Users(username=user_data.username)
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return new_user

# def get_user_by_id(db: Session, user_id: int):
#     user = db.query(Users).filter(Users.user_id == user_id).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user

# def get_user_by_username(db: Session, username: str):
#     return db.query(Users).filter(Users.username == username).first()

