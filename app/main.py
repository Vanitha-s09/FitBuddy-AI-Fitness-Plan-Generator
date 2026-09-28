from pathlib import Path

from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from .database import Base, engine
from .routes import router


BASE_DIR = Path(__file__).resolve().parent


app = FastAPI(
    title="FitBuddy",
    description="AI Fitness Plan Generator using Gemini Models",
    version="1.0.0"
)


Base.metadata.create_all(bind=engine)


templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)

app.state.templates = templates

app.include_router(router)


@app.get("/api")
async def api_home():
    return {
        "message": "Welcome to FitBuddy",
        "documentation": "/docs"
    }