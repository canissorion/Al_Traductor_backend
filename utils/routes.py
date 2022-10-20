from fastapi import FastAPI
from api.translation.controllers.translate import TranslateController


def register_routes(app: FastAPI) -> FastAPI:
    # TODO(davideliseo): Heredar controladores de una interfaz común.
    controllers = [TranslateController(app)]

    for controller in controllers:
        controller.register()

    return app
