from fastapi import FastAPI

from api.connection import ConnectionController
from api.controller import Controller
from api.languages.controllers.languages_controller import LanguagesController
from api.translation.controllers.translate_controller import TranslateController
from api.tts.controllers.tts_controller import TTSController


def register_routes(app: FastAPI) -> FastAPI:
    controllers: list[Controller] = [
        ConnectionController(app),
        TranslateController(app),
        TTSController(app),
        LanguagesController(app),
    ]

    for controller in controllers:
        controller.register()

    return app
