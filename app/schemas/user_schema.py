from typing import Optional
from pydantic import BaseModel, EmailStr, Field

# Base model for user data
class UserBase(BaseModel):
    email:EmailStr
    username: str

# user request
class UserCreate(UserBase):
    # user_id: int
    
    password: str

# user response
class User(UserBase):
    user_id: str
    

    class Config:
        from_attributes = True