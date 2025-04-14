from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine, get_db
from models import Base, Task
from schemas import TaskCreate, TaskUpdate, TaskOut
from fastapi.middleware.cors import CORSMiddleware
from typing import List

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Allow frontend CORS (adjust origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your frontend URL in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/tasks", response_model=List[TaskOut])
def get_tasks(search: str = "", db: Session = Depends(get_db)):
    query = db.query(Task)
    if search:
        query = query.filter(Task.title.ilike(f"%{search}%"))
    return query.all()

@app.post("/api/tasks", response_model=TaskOut)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    db_task = Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@app.put("/api/tasks/{task_id}", response_model=TaskOut)
def update_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    for key, value in task.dict().items():
        setattr(db_task, key, value)
    db.commit()
    db.refresh(db_task)
    return db_task

@app.delete("/api/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(db_task)
    db.commit()
    return {"detail": "Task deleted"}
