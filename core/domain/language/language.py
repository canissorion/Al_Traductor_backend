from __future__ import annotations
from abc import ABCMeta, abstractmethod
from enum import Enum, unique
from pydantic import BaseModel
from functools import cache


@unique
class LanguageModel(str, Enum):
    """
    Enumeración de los modelos de traducción disponibles.

    Atributos:
        - ML: Modelo de aprendizaje automático basado en Machine Learning.
        - CLOUD: Modelo de traducción basado en la nube.
    """

    ML = "ml"
    CLOUD = "cloud"

    @staticmethod
    @cache
    def precedence(model: LanguageModel) -> int:
        """
        Determina la precedencia de un modelo de traducción.

        Entrada:
            - model: Modelo de lenguaje
        
        Retorna: 
            - Modelo de precedencia 
        """
        precedence = {LanguageModel.ML: 0, LanguageModel.CLOUD: 1}
        return precedence[model]


@unique
class LanguageFeature(str, Enum):
    """
    Enumeración de las características de los idiomas.

    Atributos:
        - TRANSLATE: Idioma que puede ser traducido.
        - TTS: Idioma que puede ser sintetizado en voz.
    """

    TRANSLATE = "translate"
    TTS = "tts"


class LanguageModelSettings(BaseModel, metaclass=ABCMeta):
    """
    Configuración de un modelo de traducción para un idioma.

    Estos ajustes se aplican a nivel de modelo, no a nivel de idioma, por lo
    que un mismo idioma puede tener diferentes configuraciones, dependiendo de
    los modelos de traducción que soporte.

    Atributos:
        - features: Características del modelo.
        - support: Configuración de compatibilidad del modelo.
    """

    features: set[LanguageFeature] = set()

    @abstractmethod
    def includes(self, target: str) -> bool:
        pass

    @property
    @abstractmethod
    def targets(self) -> set[str]:
        pass


class LazyLanguageModelSettings(LanguageModelSettings):
    """
    Configuración de tipo lazy de un modelo de traducción para un idioma.


    Atributos:
        - include: Idiomas a incluir.
    """

    include: set[str]

    def includes(self, target: str) -> bool:
        return target in self.include

    @property
    def targets(self) -> set[str]:
        return self.include


class GreedyLanguageModelSettings(LanguageModelSettings):
    """
    Configuración de tipo greedy de un modelo de traducción para un idioma.

    Atributos:
        - include: Idiomas a excluir.
    """

    exclude: set[str] = set()

    def includes(self, target: str) -> bool:
        return target not in self.exclude

    @property
    def targets(self) -> set[str]:
        return self.exclude


class Language(BaseModel):
    """
    Información de un idioma.

    Atributos:
        - name: Nombre del idioma.
        - code: Código del idioma. Se sugiere usar el estándar ISO 639-1,
          o ISO 639-2, en su defecto.
        - models: Configuración de los modelos de traducción.
    """

    name: str
    code: str
    models: dict[
        LanguageModel,
        # El orden de la unión es importante, ya que el modelo lazy no tiene
        # valor por defecto; el greedy sí. Esto implica que si pydantic
        # encuentra el atributo "include", reconoce automáticamente el modelo
        # como lazy, si no, como greedy.
        LazyLanguageModelSettings | GreedyLanguageModelSettings,
    ] = dict()
