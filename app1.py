from fastapi import FastAPI

app = FastAPI(
    title="My FastAPI Application",
    description="This is a sample FastAPI application.",
    version="1.0.0",
    docs_url="/overview"
)

@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}

