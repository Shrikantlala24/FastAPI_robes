from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

import json
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal

app = FastAPI()

class Patient(BaseModel) :
    id : Annotated[
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
        height_in_m = self.height / 100

        return round(
            self.weight / (height_in_m ** 2),
            2
        )


# methods needed to operate on data
# 1. Load_data

def load_data():
    with open('../store.json', 'r') as f:
        return json.load(f)

# 2. Save the data
def save_data(data):
    with open('../store.json','w') as main:
        json.dump(data,main)


# Basic API endpoints
@app.get("/")
def root():
    return {"message": "Hello, World!"}

@app.get("/about")
def about():
    return {"message": "This is the about page."}


@app.get("/view")
def view_data():
    data = load_data()
    return JSONResponse(content=data)

# Here is the main endpoint :-
#? Post method to create patients

@app.post('/create')
def create_patient(patient : Patient):

    # Load the data
    data = load_data()    

    # Check if the patient ID already exists
    if patient.id in data:
        raise HTTPException(status_code=400, detail='patient already exist')

    # add new patient in the data
    data[patient.id] = patient.model_dump(exclude='id')

    # save the data in the JSON file
    save_data(data)
    return JSONResponse(
        status_code=201, 
        content = {'message':'Patient succesfully created ✅'}
        )


@app.put("/update")
def Update_patient(patient : Patient) :
    pass

