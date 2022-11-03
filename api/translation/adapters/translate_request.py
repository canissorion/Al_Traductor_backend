from pydantic import Field
from core.domain.language.language import LanguageModel
from core.kernel.request import Request


class TranslateRequest(Request):
    """
    Petición para la traducción de texto.

    Atributos:
        - source: Código del idioma de origen. Alias externo: "from".
        - target: Código del idioma de destino. Alias externo: "to".
        - model: Modelo de traducción.
        - text: Texto a traducir.
    """

    source: str = Field(alias="from")
    target: str = Field(alias="to")
    model: LanguageModel | None = None
    text: str
