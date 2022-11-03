from injector import inject

from core.kernel.validator import ValidationData, ValidationError, Validator
from core.domain.language.repositories.languages_repository import (
    LanguagesRepository,
    codes,
)


class ValidateLanguageData(ValidationData):
    """
    Información del idioma a validar.

    Atributos:
        - code: Código del idioma.
    """

    code: str


class LanguageValidator(Validator[ValidateLanguageData]):
    """
    Validador de idiomas.

    Atributos:
        - languages_repository: Repositorio de idiomas.
    """

    languages_repository: LanguagesRepository

    @inject
    def __init__(self, languages_repository: LanguagesRepository):
        self.languages_repository = languages_repository

    def validate(self, data: ValidateLanguageData) -> None:
        """
        Valida el idioma, comprobando que exista en el repositorio de idiomas.
        """
        if not (languages := self.languages_repository.all()):
            raise NoLanguagesFoundError()

        if data.code not in codes(languages):
            raise LanguageNotFoundError(data.code)


class NoLanguagesFoundError(ValidationError):
    """
    Error de validación producido cuando el repositorio de idiomas está vacío.
    """

    def __init__(self):
        super().__init__("No languages found.")


class LanguageNotFoundError(ValidationError):
    """
    Error de validación producido cuando no se encuentra un idioma en el
    repositorio.
    """

    def __init__(self, code: str):
        super().__init__(f"No language found: {{{code}}}")
