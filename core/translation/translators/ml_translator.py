from core.translation.translators.translator import Translator


class MLTranslator(Translator):
    """
    Traductor basado en modelos de machine learning.
    """

    # TODO(davideliseo): Implementar.
    def translate(self, text: str) -> str | None:
        return f"{__class__.__name__}: Not implemented."
