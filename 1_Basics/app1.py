from fastapi import FastAPI

app = FastAPI(
    title="My FastAPI Application",
    description="This is a sample FastAPI application.",
    version="1.0.0",
    docs_url="/overview"
)

@app.get("/")
async def root():
    return {"message": "Hello, World!", "answer": "it's nothing, just another key-value pair"}

@app.get("/hutt")
async def check():
    return {"message": "trail function creation"}