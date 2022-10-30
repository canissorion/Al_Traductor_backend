from core.domain.language.language import LanguageModel
from core.kernel.request import Request


class TranslateRequest(Request):
    source_language_code: str
    target_language_code: str
    model: LanguageModel | None = None
    text: str
