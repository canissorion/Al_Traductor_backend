from injector import Injector

from api.controller import Controller
from api.translation.adapters.translation_request import TranslationRequest
from api.translation.adapters.translation_response import TranslationResponse
from core.translation.features.translate_feature import TranslateFeature


class TranslateController(Controller):
    def register(self) -> None:
        @self.app.post("/translate", response_model=TranslationResponse)
        def post(request: TranslationRequest) -> TranslationResponse:
            translate = Injector().get(TranslateFeature)
            translation = translate(*request.dict().values())
            return TranslationResponse(translation=translation)
