from fastapi import FastAPI, HTTPException
import json

from pydantic import BaseModel, Field
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
        Field(...,description='Enter the Patient's City')
    ]
    age : Annotated [
        int,
        Field(..., gt = 0, lt=120, description='Enter the Patient's Age')
    ]
    gender: Annotated [
        Literal['male','female','others'],
        Field(...,description='Enter the Patient's Gender')
    ]
    height : Annotated [
        int,
        Field(..., gt=0, description='Enter the Patient hieght')
    ]
    weight : Annotated [
        int,
        Field(..., gt=0,description='Enter the Patient weight')
    ]










    
    # id: Annotated[str, Field(..., description='ID of the patient', examples=['P001'])]
    # name: Annotated[str, Field(..., description='Name of the patient')]
    # city: Annotated[str, Field(..., description='City where the patient is living')]
    # age: Annotated[int, Field(..., gt=0, lt=120, description='Age of the patient')]
    # gender: Annotated[Literal['male', 'female', 'others'], Field(..., description='Gender of the patient')]
    # height: Annotated[float, Field(..., gt=0, description='Height of the patient in mtrs')]
    # weight: Annotated[float, Field(..., gt=0, description='Weight of the patient in kgs')]


    
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