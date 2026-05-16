from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

import json

from typing import Annotated, Literal, Optional
from pydantic import BaseModel, Field, computed_field

# ----------------------------------------------------------------------------------------------------------------
# first define the schema using pydantic, it's called as model in pydantic

class PatientUpdate(BaseModel) :
    name : Annotated[
        Optional[str],
        Field(default=None)
    ]
    city : Annotated[
        Optional[str],
        Field(default=None)
    ]
    age : Annotated[
        Optional[int],
        Field(default=None, gt=0, lt=120)
    ]
    gender : Annotated[
        Optional[Literal['male','female','others']],
        Field(default=None)
    ]
    h : Annotated[
        Optional[float],
        Field(default=None, gt=0)
    ]
    w : Annotated[
        Optional[float],
        Field(default=None, gt=0)
    ]


class Patient(BaseModel) :
    id : Annotated[
        str,
        Field(..., description='enter the patient ID', examples=['P001'])
    ]
    name : Annotated[
        str,
        Field(..., description='enter the patient name')
    ]
    city : Annotated[
        str,
        Field(..., description='enter the patient city')
    ]
    age : Annotated[
        int,
        Field(..., gt=0, lt=120, description='enter the patient age')
    ]
    gender : Annotated[
        Literal['male','female','others'],
        Field(..., description='enter the patient gender from male, female , other' )
    ]
    h : Annotated[
        float,
        Field(...,gt=0, description='enter the hieght of patient in feet')
    ]
    w : Annotated[
        float,
        Field(...,gt=0, description='enter the hieght of patient in feet')
    ]

    @computed_field
    @property
    def bmi(self) -> float :
        calc = round(self.w/(self.h**2),2)
        return calc

# ----------------------------------------------------------------------------------------------------------------
# here are the operations done on the database (right now it's JSON database)

def load_data():
    with open('store.json', 'r') as f:
        return json.load(f)

def save_data(data):
    with open('store.json','w') as f:
        json.dump(data,f)

app = FastAPI()

@app.get("/")
def root():
    return {'message' : 'the root route is working'}

@app.get("/about")
def about():
    return {
        'purpose' : 'the main purpose is to serve an API-endpoint to the hospital frontend so that they can operate on Paitent data',
        'Operations' : ' CRUD '
    }

@app.get("/view")
def view_all():
    data = load_data()
    return data

@app.get("/view/{pid}")
def view_patient(pid : str) :
    data = load_data()
    if pid not in data :
        raise HTTPException(status_code=404, detail='patient not found')
    return data[pid]


    
# ----------------------------------------------------------------------------------------------------------------
# here we'll define the main create operation


@app.post("/create")
def create_patient(p : Patient) :

    # load the data
    data = load_data()

    # check if patient already exists
    if p.id in data :
        raise HTTPException(status_code= 400, detail = 'patient already exists')

    # insert the 'patient' in 'data'
    data[p.id] = p.model_dump(exclude='id')

    # save the data in the JSON database
    save_data(data)
    return JSONResponse(status_code = 201, content = {'message': 'Paitent created Succesfully and inserted in the Database'})

# ----------------------------------------------------------------------------------------------------------------
# Here is the most complicated, the UPDATE operation
@app.put("/edit/{pid}")
def update_patient(pid : str, p_update : PatientUpdate) :

    # Load the data
    data = load_data()

    # check if patient exists
    if pid not in data:
        raise HTTPException(status_code=404, detail='patient not found')

    # filling the updated values by creating 'existing' and 'updated' variables
    existing = data[pid]
    updated = p_update.model_dump(exclude_unset=True)

    for key, value in updated.items:
        existing[key] = value

        # here 'existing' has now updated values along with old values

    # now, here is the most complicated part :-

    # first -> 'id' is not in the object 
    existing['id'] = pid
    
    # second -> we need to re-initialize the computed_fields => again 'Patient' class
    final_Patient = Patient(**existing)

    # last -> add the final_patient in data
    data[pid] = final_patient.model_dump(exclude='id')

    # save the data
    save_data(data)

    # Return response\
    return JSONResponse(status_code=201, content={'message': 'Patient updated succesfully ✅'})
    