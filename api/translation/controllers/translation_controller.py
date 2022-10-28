from injector import Injector

from api.controller import Controller
from api.translation.adapters.translate_request import TranslateRequest
from api.translation.adapters.translate_response import TranslateResponse
from core.domain.translation.features.translate_feature import TranslateFeature


class TranslationController(Controller):
    def register(self) -> None:
        @self.app.post("/translate", response_model=TranslateResponse)
        def _(request: TranslateRequest) -> TranslateResponse:
            translate = Injector().get(TranslateFeature)
            translation = translate(*request.dict().values())
            return TranslateResponse(translation=translation)
