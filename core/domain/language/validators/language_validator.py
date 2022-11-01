from injector import inject

from core.kernel.validator import ValidationData, ValidationError, Validator
from core.domain.language.repositories.languages_repository import (
    LanguagesRepository,
    codes,
)


class ValidateLanguageData(ValidationData):
    code: str


class LanguageValidator(Validator[ValidateLanguageData]):
    languages_repository: LanguagesRepository

    @inject
    def __init__(self, languages_repository: LanguagesRepository):
        self.languages_repository = languages_repository

    def validate(self, data: ValidateLanguageData) -> None:
        if not (languages := self.languages_repository.all()):
            raise NoLanguagesFoundError()

        if data.code not in codes(languages):
            raise LanguageNotFoundError(data.code)


class NoLanguagesFoundError(ValidationError):
    def __init__(self):
        super().__init__("No languages found.")


class LanguageNotFoundError(ValidationError):
    def __init__(self, code: str):
        super().__init__(f"No language found: {{{code}}}")
