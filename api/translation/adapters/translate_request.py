from core.kernel.request import Request


class TranslateRequest(Request):
    source_language_code: str
    target_language_code: str
    text: str
