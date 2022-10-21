from enum import Enum
from pydantic import BaseModel

from core.language.traits.entity import LanguageTraits


class LanguageModel(Enum):
    ML = "ml"
    API = "api"


class Language(BaseModel):
    name: str
    code: str
    model: LanguageModel | None = LanguageModel.API
    traits: LanguageTraits | None = LanguageTraits()
