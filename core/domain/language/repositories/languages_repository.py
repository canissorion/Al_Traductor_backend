from typing import Callable, Iterator

from infrastructure.storage.yaml import YAMLStorage
from core.domain.language.language import (
    Language,
    LanguageModel,
    LanguageModelSettings,
)


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

    def model(
        self,
        model: LanguageModel,
        kind: type[LanguageModelSettings] = LanguageModelSettings,
    ) -> Iterator[Language]:
        """
        Devuelve los idiomas que coinciden con el modelo de consulta.

        Entradas:
            - model: Modelo de lenguaje
            - kind: Tipo de modelo de lenguaje
        
        Salida:
            - Retorna los idiomas que coinciden con el modelo de entrada
        """
        return self.filter(lambda language: type(language.models.get(model, None)) is kind)

    def filter(self, by: Callable[[Language], bool]) -> Iterator[Language]:
        """
        Devuelve los idiomas que coinciden con el filtro.

        Entrada: 
            - by: Filtrado de lenguaje
        
        Salida:
            - Retorna los idiomas que coinciden con el filtro
        """
        return filter(by, self.all())

    def get(self, code: str) -> Language | None:
        """
        Devuelve el idioma que coincide con el código.

        Entrada:
            - code: Recibe el codigo
        Salida:
            - Retorna el idioma que coincide con el código
        """
        return next(self.filter(lambda language: language.code == code), None)
