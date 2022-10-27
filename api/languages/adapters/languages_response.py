from pydantic import BaseModel
from core.domain.language.language import Language


class LanguagesResponse(BaseModel):
    languages: list[Language] | None = None
