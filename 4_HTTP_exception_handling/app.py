from fastapi import FastAPI, HTTPException, Path
import json
import requests

def load_data():
    with open('../store.json') as f:
        return json.load(f)
    
data = load_data()

app = FastAPI()

@app.get("/")
def about():
    raise HTTPException(status_code=200, detail="the route is working")

@app.get("/view")
def view_data():
    if data is None:
        raise HTTPException(status_code=404, detail="Not found")
    return data


@app.get("/view/{pid}")
def view_p(pid : str = Path(...,description="View a product by its ID")):
    if pid in data:
        return data[pid]
    raise HTTPException(status_code=404, detail="Not found")


