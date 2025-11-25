from fastapi import FastAPI
from app import router
from app.db import init_db

app = FastAPI(title="EchoPulse1314 API")

app.include_router(router)

init_db()

@app.get("/")
def root():
    return {"message": "EchoPulse1314 backend is running"}
