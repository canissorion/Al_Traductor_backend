from injector import inject
from core.domain.language.language import LanguageModel
from core.domain.language.validators.validate_language import LanguageNotFoundError

from core.kernel.validator import ValidationData, ValidationError, Validator
from core.domain.language.repositories.languages_repository import LanguagesRepository


class ValidateTranslationModelData(ValidationData):
    language_code: str
    model: LanguageModel


class ValidateTranslationModel(Validator[ValidateTranslationModelData]):
    languages_repository: LanguagesRepository

    @inject
    def __init__(self, languages_repository: LanguagesRepository):
        self.languages_repository = languages_repository

    def validate(self, data: ValidateTranslationModelData) -> None:
        language = self.languages_repository.get(data.language_code)
        if language is None:
            raise LanguageNotFoundError(data.language_code)
        elif data.model not in language.models:
            raise ModelNotSupportedByLanguageError(data.model, data.language_code)


class ModelNotSupportedByLanguageError(ValidationError):
    def __init__(self, model: LanguageModel, language_code: str):
        super().__init__(
            f"Model {{{model}}} not supported by {{{language_code}}} language."
        )
