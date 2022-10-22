from pydantic import BaseModel
from core.language.language import Language


class LanguagesResponse(BaseModel):
    languages: list[Language] | None = None
