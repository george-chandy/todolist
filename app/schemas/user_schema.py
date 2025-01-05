from typing import Optional
from pydantic import BaseModel

# Base model for user data
class UserBase(BaseModel):
    email:str
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