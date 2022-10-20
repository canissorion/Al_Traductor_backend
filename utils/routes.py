from fastapi import FastAPI
from api.translation.controllers.translate import TranslateController
from api.tts.controllers.tts import TTSController


def register_routes(app: FastAPI) -> FastAPI:
    # TODO(davideliseo): Heredar controladores de una interfaz común.
    controllers = [
        TranslateController(app),
        TTSController(app),
    ]

    for controller in controllers:
        controller.register()

    return app
