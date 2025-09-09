from fastapi import FastAPI
from app.models.extensions import db, migrate, cors
from .routes import main_router

def create_app():
    app = FastAPI()
    app.include_router(main_router)
    return app

app = create_app()
