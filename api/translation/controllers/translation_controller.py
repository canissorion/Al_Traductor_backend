from injector import Injector
from fastapi import HTTPException

from api.controller import Controller
from api.translation.adapters.translate_port import TranslatePort
from api.translation.adapters.translate_request import TranslateRequest
from api.translation.adapters.translate_response import TranslateResponse
from core.domain.translation.features.translate_feature import TranslateFeature


class TranslationController(Controller):
    def register(self) -> None:
        @self.app.post("/translate", response_model=TranslateResponse)
        def _(request: TranslateRequest) -> TranslateResponse:
            injector = Injector()
            translate = injector.get(TranslateFeature)
            port = injector.get(TranslatePort)

            try:
                translation = translate.execute(input=port.input(request))
                return port.output(output=translation)
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
