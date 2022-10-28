from core.kernel.request import Request


class TTSRequest(Request):
    language_code: str
    text: str
