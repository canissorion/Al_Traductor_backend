from core.domain.translation.repositories.translators.translator import Translator


class CloudTranslator(Translator):
    """
    Traductor en la nube basado en la API de Google Translate.

    Atributos:
        - source: Idioma de origen.
        - target: Idioma de destino.
    """

    # TODO(davideliseo): Implementar.
    def translate(self, text: str) -> str | None:
        return f"{__class__.__name__}: Not implemented."
