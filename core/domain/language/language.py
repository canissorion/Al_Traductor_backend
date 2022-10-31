from enum import Enum
from pydantic import BaseModel


class LanguageModel(str, Enum):
    ML = "ml"
    CLOUD = "cloud"


class LanguageFeature(str, Enum):
    TRANSLATE = "translate"
    TTS = "tts"


class LanguageAvailabilityMode(str, Enum):
    INCLUDE = "include"
    EXCLUDE = "exclude"


class LanguageAvailability(BaseModel):
    mode: LanguageAvailabilityMode | None = LanguageAvailabilityMode.EXCLUDE
    sources: set[str] = set()
    targets: set[str] = set()


class LanguageModelSettings(BaseModel):
    features: set[LanguageFeature] = set()
    availability: LanguageAvailability | bool = True


class Language(BaseModel):
    name: str
    code: str
    models: dict[LanguageModel, LanguageModelSettings | bool] = dict()
