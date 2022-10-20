from pydantic import BaseModel


class LanguageTraits(BaseModel):
    source: bool | None = False
    target: bool | None = False
    tts: bool | None = False
