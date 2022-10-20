import typing as t
from fastapi import FastAPI, types as ft
from api.translation.adapters.request import TranslationRequest
from api.translation.adapters.response import TranslationResponse
from core.translation.features.translate import TranslateFeature


class TranslateController:
    # FIXME(davideliseo): Dependencia de capa externa.
    app: FastAPI

    def __init__(self, app: FastAPI):
        self.app = app

    def register(self) -> ft.DecoratedCallable:
        def method(request: TranslationRequest) -> TranslationResponse:
            translate = TranslateFeature()
            translation = translate(*request.dict().values())
            return TranslationResponse(translation=translation)

        post: t.Callable[
            [ft.DecoratedCallable],
            ft.DecoratedCallable,
        ] = self.app.post("/translate", response_model=TranslationResponse)

        return post(method)
