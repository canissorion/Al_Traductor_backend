import typing as t
from fastapi import FastAPI, types as ft

from api.tts.adapters.request import TTSRequest
from api.tts.adapters.response import TTSResponse
from core.synthesis.features.synthesize import SynthesizeFeature


class TTSController:
    # FIXME(davideliseo): Dependencia de capa externa.
    app: FastAPI

    def __init__(self, app: FastAPI):
        self.app = app

    def register(self) -> ft.DecoratedCallable:
        def method(request: TTSRequest) -> TTSResponse:
            synthesize = SynthesizeFeature()
            speech = synthesize(*request.dict().values())
            return TTSResponse(speech=speech)

        post: t.Callable[
            [ft.DecoratedCallable],
            ft.DecoratedCallable,
        ] = self.app.post("/tts", response_model=TTSResponse)

        return post(method)
