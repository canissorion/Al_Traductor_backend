from pydantic import Field
from core.kernel.request import Request


class TTSRequest(Request):
    """
    Petición para la síntesis de voz.

    Atributos:
        - source: Código del idioma de origen. Alias externo: "language".
        - text: Texto a sintetizar.
    """

    source: str = Field(alias="language")
    text: str
