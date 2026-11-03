from fastapi import FastAPI
from app.routers import router

app = FastAPI(title="FastAPI GitOps Project")

app.include_router(router)


@app.get("/")
def home():
    return {"message": "FastAPI + PostgreSQL connected"}


@app.get("/health")
def health():
    return {"status": "healthy"}