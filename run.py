from app import create_app
from app.routes.api import main_router
from app.routes.ui import ui_router
from app.routes.training import training_router

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)