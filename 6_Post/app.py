from fastapi import FastAPI, HTTPException
import json

from pydantic import BaseModel
from typing import Optional

app = FastAPI()

def load_data():
    with open('../store.json', 'r') as f:
        return json.load(f)
    
data = load_data()    

@app.get("/")
def root():
    return {"message": "Hello, World!"}

@app.get("/about")
def about():
    return {"message": "This is the about page."}

@app.post('/create')
def create_patient(patient : Patient):