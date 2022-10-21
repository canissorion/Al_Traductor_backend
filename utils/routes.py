from fastapi import FastAPI

from api.connection import ConnectionController
from api.languages.controllers.languages import LanguagesController
from api.translation.controllers.translate import TranslateController
from api.tts.controllers.tts import TTSController


def register_routes(app: FastAPI) -> FastAPI:
    # TODO(davideliseo): Abstraer controladores a una interfaz común.
    controllers = [
        ConnectionController(app),
        TranslateController(app),
        TTSController(app),
        LanguagesController(app),
    ]

    for controller in controllers:
        controller.register()

    return app
