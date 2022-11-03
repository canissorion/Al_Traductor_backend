from pydantic import BaseModel
from core.domain.language.language import Language


class LanguagesResponse(BaseModel):
    """
    Respuesta de la API con la lista de lenguajes.
    """

    languages: list[Language] | None = None
