from core.domain.translation.repositories.translators.translator import Translator


class MLTranslator(Translator):
    """
    Traductor basado en modelos de machine learning.

    Atributos:
        - source: Idioma de origen.
        - target: Idioma de destino.
    """

    # TODO(davideliseo): Implementar.
    def translate(self, text: str) -> str | None:
        return f"{__class__.__name__}: Not implemented."
