from enum import Enum
from pydantic import BaseModel


class LanguageTraits(BaseModel):
    source: bool | None = False
    target: bool | None = False
    tts: bool | None = False


class LanguageModel(str, Enum):
    ML = "ml"
    CLOUD = "cloud"


class Language(BaseModel):
    name: str
    code: str
    models: list[LanguageModel] = [LanguageModel.CLOUD]
    traits: LanguageTraits | None = LanguageTraits()
