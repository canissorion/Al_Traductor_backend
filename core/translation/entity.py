from pydantic import BaseModel


class Translation(BaseModel):
    source_language_code: str
    target_language_code: str
    source_text: str
    translated_text: str | None = None
