from core.domain.translation.repositories.translators.translator import Translator
from googletrans import Translator as GoogleTranslator  # pyright: ignore


class CloudTranslator(Translator):
    """
    Traductor en la nube basado en la API de Google Translate.

    Atributos:
        - source: Idioma de origen.
        - target: Idioma de destino.

    Salidas:
        retorna la traduccion de texto.
    """

    def translate(self, text: str) -> str | None:
        return GoogleTranslator().translate(text, self.target, self.source).text  # pyright: ignore
