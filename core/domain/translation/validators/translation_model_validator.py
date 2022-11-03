from injector import inject
from core.domain.language.language import LanguageModel
from core.domain.language.validators.language_validator import LanguageNotFoundError

from core.kernel.validator import ValidationData, ValidationError, Validator
from core.domain.language.repositories.languages_repository import LanguagesRepository


class ValidateTranslationModelData(ValidationData):
    """
    Información del modelo de traducción a validar.

    Atributos:
        - code: Código del idioma.
        - model: Modelo de traducción.
    """

    code: str
    model: LanguageModel


class TranslationModelValidator(Validator[ValidateTranslationModelData]):
    """
    Validador de modelo de traducción.

    Atributos:
        - languages_repository: Repositorio de idiomas.
    """

    languages_repository: LanguagesRepository

    @inject
    def __init__(self, languages_repository: LanguagesRepository):
        self.languages_repository = languages_repository

    def validate(self, data: ValidateTranslationModelData) -> None:
        """
        Valida el modelo de traducción, comprobando que el idioma lo soporte.
        """
        if (language := self.languages_repository.get(data.code)) is None:
            raise LanguageNotFoundError(data.code)
        elif data.model not in language.models:
            raise ModelNotSupportedByLanguageError(data.model, data.code)


class ModelNotSupportedByLanguageError(ValidationError):
    """
    Error de validación producido cuando el idioma no soporta el modelo de traducción.
    """

    def __init__(self, model: LanguageModel, code: str):
        super().__init__(f"Model {{{model}}} is not supported by {{{code}}} language.")


class ModelNotSupportedByTranslationError(ValidationError):
    """
    Error de validación producido cuando la traducción entre dos idiomas no se
    puede realizar con el modelo de traducción.
    """

    def __init__(self, model: LanguageModel, source: str, target: str):
        super().__init__(
            f"Model {{{model}}} is not supported for the {{{source}}} to {{{target}}} translation."
        )
