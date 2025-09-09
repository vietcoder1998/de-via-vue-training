from fastapi import FastAPI
from app.models.extensions import db, migrate, cors
from app.routes.api import main_router
from app.routes.ui import ui_router
from app.routes.training import training_router


def create_app():
    app = FastAPI()
    app.include_router(main_router, tags=["API"])
    app.include_router(ui_router, tags=["UI"])
    app.include_router(training_router, tags=["Training"])

    return app
