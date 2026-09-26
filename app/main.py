from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.routes import router


BASE_DIR = Path(__file__).resolve().parent.parent


# Create required folders
settings.panels_dir.mkdir(parents=True, exist_ok=True)
settings.exports_dir.mkdir(parents=True, exist_ok=True)


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="ComicCraft AI Comic Story Creator",
)


# Static files
app.mount(
    "/static",
    StaticFiles(directory=str(BASE_DIR / "static")),
    name="static",
)


# Routes
app.include_router(router)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "app": settings.app_name,
    }