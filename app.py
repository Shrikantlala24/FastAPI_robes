from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

tasks = []

class Task(BaseModel):
    title: str

@app.post("/tasks")
def add_task(task: Task):
    tasks.append(task.title)
    return {"message": "Task added", "tasks": tasks}

@app.get("/tasks")
def get_tasks():
    return {"tasks": tasks}