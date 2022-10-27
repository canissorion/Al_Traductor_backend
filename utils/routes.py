from fastapi import FastAPI
from injector import Injector, singleton
from typing import Type

from api.connection import ConnectionController
from api.controller import Controller
from api.languages.controllers.languages_controller import LanguagesController
from api.translation.controllers.translate_controller import TranslateController
from api.tts.controllers.tts_controller import TTSController


def register_routes(app: FastAPI) -> FastAPI:
    injector = Injector(lambda binder: binder.bind(FastAPI, to=app, scope=singleton))

    controllers: list[Type[Controller]] = [
        ConnectionController,
        TranslateController,
        TTSController,
        LanguagesController,
    ]

    for controller in controllers:
        injector.get(controller).register()

    return app
