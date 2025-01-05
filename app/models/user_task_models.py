from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String, Enum,ForeignKey
from app.database.database import Base
from app.schemas.user_task import TaskStatus
from sqlalchemy.orm import relationship


class Tasks(Base):
    __tablename__ = 'tasks'
    reference_id=Column(Integer)
    task_id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    todolist = Column(String)
    status = Column(Enum(TaskStatus), default=TaskStatus.PENDING)
