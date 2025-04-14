from sqlalchemy import Column, Integer, String, Boolean
from database import Base, Task

class Book(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, default="")
    completed = Column(Boolean, default=False)
