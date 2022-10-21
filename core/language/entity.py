from enum import Enum
from pydantic import BaseModel

from core.language.traits.entity import LanguageTraits


class LanguageModel(str, Enum):
    ML = "ml"
    CLOUD = "cloud"


class Language(BaseModel):
    name: str
    code: str
    model: LanguageModel | None = LanguageModel.CLOUD
    traits: LanguageTraits | None = LanguageTraits()
