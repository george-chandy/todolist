import uuid
from sqlalchemy import UUID, Column, Date, DateTime, ForeignKey, Integer, String, Enum,ForeignKey
from app.database.database import Base
from app.schemas.user_task import TaskStatus
from sqlalchemy.orm import relationship



class Users(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, nullable=False, unique=True)
    reference_id = Column(String, unique=True)
    email = Column(String, unique=True, nullable=True)
    name = Column(String, nullable=True)
    

    

class Tasks(Base):
    __tablename__ = 'tasks'
    reference_id=Column(String)
    task_id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    todolist = Column(String)
    status = Column(Enum(TaskStatus), default=TaskStatus.PENDING)



    
    