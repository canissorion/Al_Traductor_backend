from pydantic import BaseModel


class TranslateRequest(BaseModel):
    source_language_code: str
    target_language_code: str
    text: str
