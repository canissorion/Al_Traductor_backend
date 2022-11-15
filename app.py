from fastapi import FastAPI

from utils.routes import register_routes


def create_app() -> FastAPI:
    """
    Inicializa la aplicación.
    """
    app = FastAPI()
    app = register_routes(app)
    return app
