from core.kernel.response import Response


# TODO(davideliseo): Definir.
class TTSResponse(Response):
    speech: str | None = None
