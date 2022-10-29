from injector import inject

from core.kernel.validator import ValidationData, ValidationError, Validator
from core.domain.language.repositories.languages_repository import LanguagesRepository


class ValidateLanguageCodeData(ValidationData):
    language_code: str


class ValidateLanguageCode(Validator[ValidateLanguageCodeData]):
    languages_repository: LanguagesRepository

    @inject
    def __init__(self, languages_repository: LanguagesRepository):
        self.languages_repository = languages_repository

    def validate(self, data: ValidateLanguageCodeData) -> None:
        if (languages := self.languages_repository.get_languages()) is None:
            raise NoLanguagesFoundError()

        language_codes = {language.code for language in languages}

        if data.language_code not in language_codes:
            raise InvalidLanguageCodeError(data.language_code)


class InvalidLanguageCodeError(ValidationError):
    def __init__(self, language_code: str):
        super().__init__(f"Invalid language code: {language_code}")


class NoLanguagesFoundError(ValidationError):
    def __init__(self):
        super().__init__("No languages found.")
