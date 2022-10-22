from api.controller import Controller

from api.translation.adapters.translation_request import TranslationRequest
from api.translation.adapters.translation_response import TranslationResponse
from core.language.repositories.languages_repository import LanguagesRepository
from core.translation.features.translate_feature import TranslateFeature


class TranslateController(Controller):
    def register(self) -> None:
        @self.app.post("/translate", response_model=TranslationResponse)
        def post(request: TranslationRequest) -> TranslationResponse:
            translate = TranslateFeature(languages_repository=LanguagesRepository())
            translation = translate(*request.dict().values())
            return TranslationResponse(translation=translation)
