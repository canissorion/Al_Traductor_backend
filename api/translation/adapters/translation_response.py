from pydantic import BaseModel


class TranslationResponse(BaseModel):
    translation: str | None = None
