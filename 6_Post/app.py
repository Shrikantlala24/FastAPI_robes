from fastapi import FastAPI, HTTPException
import json

from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal

app = FastAPI()

class Patient(BaseModel) :
    pid : Annotated[
        str,
        Field(...,description='Enter the Patient ID', examples=['P001'])
    ]
    name : Annotated [
        str,
        Field(...,description='Enter the Patient name')
    ]
    city : Annotated [
        str,
        Field(...,description='Enter the Patient City')
    ]
    age : Annotated [
        int,
        Field(..., gt = 0, lt=120, description='Enter the Patient Age')
    ]
    gender: Annotated [
        Literal['male','female','others'],
        Field(...,description='Enter the Patient Gender')
    ]
    height : Annotated [
        int,
        Field(..., gt=0, description='Enter the Patient hieght')
    ]
    weight : Annotated [
        int,
        Field(..., gt=0,description='Enter the Patient weight')
    ]

    @computed_field
    @property
    def bmi(self) -> float:
        return round(
            self.weight/(self.height **2),
            2
        )
    
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
    pass