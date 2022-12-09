from core.kernel.response import Response


class TranslateResponse(Response):
    """
    Respuesta de la traducción de texto.

    Atributos:
        - translation: Texto traducido.
    """

    translation: str | None = None
