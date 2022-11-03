from injector import inject, Injector
from core.domain.translation.validators.translation_model_validator import (
    TranslationModelValidator,
    ValidateTranslationModelData,
)

from core.kernel.port import Port
from core.domain.language.repositories.languages_repository import LanguagesRepository

from api.translation.adapters.translate_request import TranslateRequest
from api.translation.adapters.translate_response import TranslateResponse

from core.domain.translation.features.translate_feature import (
    TranslateFeatureInput,
    TranslateFeatureOutput,
)

from core.domain.language.validators.language_validator import (
    LanguageValidator,
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
    """
    Puertos de entrada y salida para la traducción de texto.

    Atributos:
        - languages_repository: Repositorio de idiomas.
    """

    languages_repository: LanguagesRepository

    @inject
    def __init__(self, languages_repository: LanguagesRepository) -> None:
        self.languages_repository = languages_repository
        super().__init__()

    def input(self, request: TranslateRequest) -> TranslateFeatureInput:
        """
        Transforma y valida la petición de un controlador en una entrada para
        la característica de traducción.
        """
        injector = Injector()
        language_validator = injector.get(LanguageValidator)
        translation_model_validator = injector.get(TranslationModelValidator)

        for code in (request.source, request.target):
            language_validator.validate(
                ValidateLanguageData(code=code),
            )

            if request.model is not None:
                translation_model_validator.validate(
                    ValidateTranslationModelData(code=code, model=request.model),
                )

        return TranslateFeatureInput(**dict(request))

    def output(self, output: TranslateFeatureOutput | None) -> TranslateResponse:
        """
        Transforma la salida de la característica de traducción en una
        respuesta para un controlador.
        """
        return TranslateResponse(
            translation=str(output.translation) if output is not None else None,
        )
