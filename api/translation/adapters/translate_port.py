from injector import inject, Injector

from core.kernel.port import Port
from core.domain.language.repositories.languages_repository import LanguagesRepository

from api.translation.adapters.translate_request import TranslateRequest
from api.translation.adapters.translate_response import TranslateResponse

from core.domain.translation.features.translate_feature import (
    TranslateFeatureInput,
    TranslateFeatureOutput,
)

from core.domain.language.validators.validate_language import (
    ValidateLanguage,
    ValidateLanguageData,
)


class TranslatePort(
    Port[
        TranslateRequest,
        TranslateResponse,
        TranslateFeatureInput,
        TranslateFeatureOutput,
    ]
):
    languages_repository: LanguagesRepository

    @inject
    def __init__(self, languages_repository: LanguagesRepository) -> None:
        self.languages_repository = languages_repository
        super().__init__()

    def input(self, request: TranslateRequest) -> TranslateFeatureInput:
        injector = Injector()
        validator = injector.get(ValidateLanguage)

        for language_code in (
            request.source_language_code,
            request.target_language_code,
        ):
            data = ValidateLanguageData(language_code=language_code)
            validator.validate(data)

        return TranslateFeatureInput(**dict(request))

    def output(self, output: TranslateFeatureOutput | None) -> TranslateResponse:
        return TranslateResponse(
            translation=str(output.value) if output is not None else None
        )
