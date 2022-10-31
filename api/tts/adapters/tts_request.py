from pydantic import Field
from core.kernel.request import Request


class TTSRequest(Request):
    source: str = Field(alias="language")
    text: str
