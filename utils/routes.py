from fastapi import FastAPI
from injector import Injector, singleton
from typing import Type

from api.connection import ConnectionController
from api.controller import Controller
from api.languages.controllers.languages_controller import LanguagesController
from api.translation.controllers.translation_controller import TranslationController
from api.tts.controllers.tts_controller import TTSController


def register_routes(app: FastAPI) -> None:
    """
    Registra las rutas de la API.
    """
    # Inyecta las dependencias de la aplicación en los controladores.
    injector = Injector(
        lambda binder: binder.bind(FastAPI, to=app, scope=singleton),
    )

    controllers: list[Type[Controller]] = [
        ConnectionController,
        TranslationController,
        TTSController,
        LanguagesController,
    ]

    for controller in controllers:
        injector.get(controller).register()
