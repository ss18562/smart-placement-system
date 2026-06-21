from fastapi import FastAPI
from app.db.database import engine
from app.db.base import Base
from app.api.user import router as user_router
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Smart Placement Preparation System",
    description="AI-Powered Placement Readiness Platform",
    version="1.0.0"
)
@app.get("/")
def root():
    return {
        "message": "Smart Placement Preparation System API is running"
    }
app.include_router(user_router)
    