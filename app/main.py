from fastapi import FastAPI
from app.api.v1.router import api_router

app = FastAPI(
    title="My Web API",
    version="1.0.0",
)


@app.get("/")
def root():
    return {
        "message": "API is running"
    }


app.include_router(api_router)
