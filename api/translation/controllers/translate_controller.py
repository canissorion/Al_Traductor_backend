import typing as t
from fastapi import FastAPI, types as ft

from api.translation.adapters.translation_request import TranslationRequest
from api.translation.adapters.translation_response import TranslationResponse
from core.language.repositories.languages_repository import LanguagesRepository
from core.translation.features.translate_feature import TranslateFeature


class TranslateController:
    # FIXME(davideliseo): Dependencia de capa externa.
    app: FastAPI

    def __init__(self, app: FastAPI):
        self.app = app

    def register(self) -> ft.DecoratedCallable:
        def method(request: TranslationRequest) -> TranslationResponse:
            translate = TranslateFeature(languages_repository=LanguagesRepository())
            translation = translate(*request.dict().values())
            return TranslationResponse(translation=translation)

        decorate = self.app.post("/translate", response_model=TranslationResponse)
        return decorate(method)