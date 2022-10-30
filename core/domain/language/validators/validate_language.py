from injector import inject

from core.kernel.validator import ValidationData, ValidationError, Validator
from core.domain.language.repositories.languages_repository import LanguagesRepository


class ValidateLanguageData(ValidationData):
    language_code: str


class ValidateLanguage(Validator[ValidateLanguageData]):
    languages_repository: LanguagesRepository

    @inject
    def __init__(self, languages_repository: LanguagesRepository):
        self.languages_repository = languages_repository

    def validate(self, data: ValidateLanguageData) -> None:
        if not (languages := self.languages_repository.all()):
            raise NoLanguagesFoundError()

        language_codes = {language.code for language in languages}
        if data.language_code not in language_codes:
            raise NoLanguageFoundError(data.language_code)


class NoLanguagesFoundError(ValidationError):
    def __init__(self):
        super().__init__("No languages found.")


class NoLanguageFoundError(ValidationError):
    def __init__(self, language_code: str):
        super().__init__(f"No language found: {{{language_code}}}")
