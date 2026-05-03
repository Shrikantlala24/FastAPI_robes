# right now we'll make a simple to-do app as for trial

from fastapi import FastAPI
from pydantic import BaseModel

task_list = []


class task(BaseModel):
    title : str
    
app = FastAPI()

@app.post("/tasks")
def add_task(task : Task):
    task_list.append()


@app.get("/tasks")
def get_tasks():
    return {"Tasks :",task_list}