import typing as t
from fastapi import FastAPI, types as ft

from api.languages.adapters.response import LanguagesResponse
from core.language.repository.languages import LanguagesRepository


class LanguagesController:
    # FIXME(davideliseo): Dependencia de capa externa.
    app: FastAPI

    def __init__(self, app: FastAPI):
        self.app = app

    def register(self) -> ft.DecoratedCallable:
        def method() -> LanguagesResponse:
            repository = LanguagesRepository()
            languages = repository.get_languages()
            return LanguagesResponse(languages=languages)

        decorate = self.app.get("/languages", response_model=LanguagesResponse)
        return decorate(method)
