from injector import inject
from core.domain.language.language import LanguageModel
from core.domain.language.validators.language_validator import LanguageNotFoundError

from core.kernel.validator import ValidationData, ValidationError, Validator
from core.domain.language.repositories.languages_repository import LanguagesRepository


class ValidateTranslationModelData(ValidationData):
    code: str
    model: LanguageModel


class TranslationModelValidator(Validator[ValidateTranslationModelData]):
    languages_repository: LanguagesRepository

    @inject
    def __init__(self, languages_repository: LanguagesRepository):
        self.languages_repository = languages_repository

    def validate(self, data: ValidateTranslationModelData) -> None:
        if (language := self.languages_repository.get(data.code)) is None:
            raise LanguageNotFoundError(data.code)
        elif data.model not in language.models:
            raise ModelNotSupportedByLanguageError(data.model, data.code)


class ModelNotSupportedByLanguageError(ValidationError):
    def __init__(self, model: LanguageModel, code: str):
        super().__init__(f"Model {{{model}}} not supported by {{{code}}} language.")
