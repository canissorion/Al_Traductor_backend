from core.domain.translation.repositories.translators.translator import Translator
from googletrans import Translator as GoogleTranslator

class CloudTranslator(Translator):
    """
    Traductor en la nube basado en la API de Google Translate.

    Atributos:
        - source: Idioma de origen.
        - target: Idioma de destino.
    """

    # TODO(davideliseo): Implementar.
    def translate(self, text: str) -> str | None:
        response = GoogleTranslator().translate(text,self.target,self.source).text
        return f"{__class__.__name__}: "+response
