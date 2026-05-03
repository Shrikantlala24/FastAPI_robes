from fastapi import FastAPI
# from pydantic import BaseModel
import json

def load_data():
    with open('store.json') as f:
        data = json.load(f)
    return data

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/about")
def abot_info():
    return {"mesafe" : "this is a full y funcibdsubve igfbue"}

@app.get("/view")
def view():
    data = load_data()

    return data