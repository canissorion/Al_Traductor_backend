from __future__ import annotations
from enum import Enum, unique
from pydantic import BaseModel
import functools


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
    @functools.cache
    def precedence(model: LanguageModel) -> int:
        """
        Determina la precedencia de un modelo de traducción.
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


@unique
class LanguageSupportMode(str, Enum):
    """
    Enumeración de los modos de compatibilidad de los idiomas.

    Atributos:
        - INCLUDE: Modo de compatibilidad de inclusión, o lazy. Indica que el
          idioma es compatible sólo con los idiomas incluidos explícitamente.
        - EXCLUDE: Modo de compatibilidad de exclusión, o greedy. Indica que el
          idioma es compatible con todos los idiomas excepto los excluidos
          explícitamente.
    """

    INCLUDE = "include"
    EXCLUDE = "exclude"


class LanguageSupport(BaseModel):
    """
    Configuración de compatibilidad de un idioma.

    Dependiendo del modo de compatibilidad, se incluyen o excluyen los idiomas
    de la configuración.

    Atributos:
        mode: Modo de compatibilidad.
        targets: Lista de códigos de idiomas compatibles o incompatibles.
    """

    mode: LanguageSupportMode = LanguageSupportMode.EXCLUDE
    targets: set[str] = set()


class LanguageModelSettings(BaseModel):
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
    support: LanguageSupport = LanguageSupport()

    def includes(self, target: str) -> bool:
        """
        Determina si un idioma es compatible de acuerdo a la configuración.
        """
        match self.support.mode:
            case LanguageSupportMode.EXCLUDE:
                return target not in self.support.targets
            case LanguageSupportMode.INCLUDE:
                return target in self.support.targets


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
    models: dict[LanguageModel, LanguageModelSettings] = dict()
