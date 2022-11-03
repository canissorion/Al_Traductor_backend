from core.kernel.response import Response


class TTSResponse(Response):
    """
    Respuesta de la sintetización de voz.

    TODO(davideliseo): Definir.
    """

    speech: str | None = None
