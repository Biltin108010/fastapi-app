from pydantic import BaseModel

class TaskCreate(BaseModel):
    title: str
    description: str = ""
    completed: bool = False

class TaskUpdate(BaseModel):
    title: str
    description: str = ""
    completed: bool

class TaskOut(TaskCreate):
    id: int

    class Config:
        orm_mode = True
