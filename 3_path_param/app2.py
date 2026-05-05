from fastapi import FastAPI
import json

# import requests


def load_data():
    with open('../store.json') as f:
        data = json.load(f)
    return data

data = load_data()

app = FastAPI()

@app.get("/view")
def view_data():
    
    return data

@app.get("/view/{p_id}")
def view_product(p_id : str):
    if p_id in data:
        return data[p_id];
    return {'error': 'product not found'}
