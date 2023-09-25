from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base

app = FastAPI(
    title="Домашнее задание к пятому семинару",
    description="API для управления списком задач",
    version="0.1"
)

engine = create_engine("sqlite:///tasks.db")
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


class Task(BaseModel):
    id: int
    title: str
    description: str
    completed: bool = False


class TaskIn(BaseModel):
    title: str
    description: str


class TaskOut(BaseModel):
    id: int
    title: str
    description: str
    completed: bool = False


Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/tasks", response_model=Dict[int, TaskOut], tags=["tasks"])
async def get_tasks(db=Depends(get_db)):
    """
    Возвращает список всех задач
    """
    tasks = db.query(Task).all()
    return {task.id: TaskOut.from_orm(task) for task in tasks}


@app.get("/tasks/{task_id}", response_model=TaskOut, tags=["tasks"])
async def get_task(task_id: int, db=Depends(get_db)):
    """
    Возвращает задачу с указанным идентификатором
    """
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskOut.from_orm(task)


@app.post("/tasks", response_model=TaskOut, tags=["tasks"])
async def create_task(task: TaskIn, db=Depends(get_db)):
    """
    Добавляет новую задачу
    """
    db_task = Task(title=task.title, description=task.description)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return TaskOut.from_orm(db_task)


@app.put("/tasks/{task_id}", response_model=TaskOut, tags=["tasks"])
async def update_task(task_id: int, task: Task, db=Depends(get_db)):
    """
    Обновляет задачу с указанным идентификатором
    """
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    db_task.title = task.title
    db_task.description = task.description
    db_task.completed = task.completed
    db.commit()
    db.refresh(db_task)
    return TaskOut.from_orm(db_task)


@app.delete("/tasks/{task_id}", response_model=Dict[str, str], tags=["tasks"])
async def delete_task(task_id: int, db=Depends(get_db)):
    """
    Удаляет задачу с указанным идентификатором
    """
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(db_task)
    db.commit()
    return {"message": "Task deleted successfully"}
