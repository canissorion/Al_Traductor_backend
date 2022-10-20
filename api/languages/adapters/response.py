from pydantic import BaseModel
from core.language.entity import Language


class LanguagesResponse(BaseModel):
    languages: list[Language]
