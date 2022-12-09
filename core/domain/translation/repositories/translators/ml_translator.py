from core.domain.translation.repositories.translators.translator import Translator
from services.translator.model import build_translator, TranslatorBuilderMode


class MLTranslator(Translator):
    """
    Traductor basado en modelos de machine learning.

    Atributos:
        - source: Idioma de origen.
        - target: Idioma de destino.
    """

    # TODO(davideliseo): Implementar.
    def translate(self, text: str) -> str | None:
        translator = build_translator(self.source, self.target, mode=TranslatorBuilderMode.LOAD)
        return translator(text)
