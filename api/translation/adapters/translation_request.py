from pydantic import BaseModel


class TranslationRequest(BaseModel):
    source_language_code: str
    target_language_code: str
    text: str
