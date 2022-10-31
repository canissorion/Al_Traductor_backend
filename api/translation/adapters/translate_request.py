from pydantic import Field
from core.domain.language.language import LanguageModel
from core.kernel.request import Request


class TranslateRequest(Request):
    source: str = Field(alias="from")
    target: str = Field(alias="to")
    model: LanguageModel | None = None
    text: str
