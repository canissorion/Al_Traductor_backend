from pydantic import BaseModel

from core.language.traits.entity import LanguageTraits


class Language(BaseModel):
    name: str
    code: str
    traits: LanguageTraits | None = LanguageTraits()
