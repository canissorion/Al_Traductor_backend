from pydantic import BaseModel


class TTSRequest(BaseModel):
    language_code: str
    text: str
