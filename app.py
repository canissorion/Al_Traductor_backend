from fastapi import FastAPI
from utils.cors import register_cors

from utils.routes import register_routes


def create_app() -> FastAPI:
    """
    Inicializa la aplicación.
    """
    app = FastAPI()

    register_routes(app)
    register_cors(app)

    return app
