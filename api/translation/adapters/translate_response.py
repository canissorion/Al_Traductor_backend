from core.kernel.response import Response


class TranslateResponse(Response):
    translation: str | None = None
