from typing import Callable, Iterator
from core.domain.language.language import Language, LanguageModel
from infrastructure.storage.yaml import YAMLStorage


def codes(languages: Iterator[Language]) -> Iterator[str]:
    return (language.code for language in languages)


class LanguagesRepository:
    """
    Repositorio de idiomas.

    Atributos:
        - filename: Nombre del archivo YAML con la definición de los idiomas.
        - storage: Almacenamiento de idiomas.

    TODO(davideliseo): Convertir a singleton.
    """

    filename = "core/domain/language/repositories/sources/languages_source.yaml"
    storage = YAMLStorage(filename=filename)

    def all(self) -> Iterator[Language]:
        """
        Devuelve todos los idiomas del repositorio.
        """
        if (languages := self.storage.read()) is None:
            return iter(())

        return (Language(code=code, **language) for code, language in languages.items())

    def query(self, model: LanguageModel) -> Iterator[Language]:
        """
        Devuelve los idiomas que coinciden con el modelo de consulta.
        """
        return self.filter(lambda language: model in language.models)

    def filter(self, by: Callable[[Language], bool]) -> Iterator[Language]:
        """
        Devuelve los idiomas que coinciden con el filtro.
        """
        return filter(by, self.all())

    def get(self, code: str) -> Language | None:
        """
        Devuelve el idioma que coincide con el código.
        """
        return next(self.filter(lambda language: language.code == code), None)
