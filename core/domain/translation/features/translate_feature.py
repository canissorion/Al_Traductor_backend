from typing import Iterator
from injector import inject, Injector
from functools import reduce

from core.kernel.feature.feature import Feature
from core.kernel.feature.feature_input import FeatureInput
from core.kernel.feature.feature_output import FeatureOutput

from core.domain.language.language import LanguageModel
from core.domain.language.repositories.languages_repository import LanguagesRepository

from core.domain.translation.repositories.translators.translator import Translator
from core.domain.translation.repositories.translators.ml_translator import MLTranslator
from core.domain.translation.repositories.translators.cloud_translator import CloudTranslator
from core.domain.translation.repositories.translation_graph import Edge, TranslationGraph


class TranslateFeatureInput(FeatureInput):
    """
    Datos de entrada de la característica de traducción.

    Atributos:
        - text: Texto a traducir.
        - source: Idioma del texto a traducir.
        - target: Idioma al que se quiere traducir el texto.
        - model: Modelo de traducción a utilizar. Si no se especifica, se
          utilizará el modelo más adecuado.
    """

    source: str
    target: str
    text: str
    model: LanguageModel | None = None


class TranslateFeatureOutput(FeatureOutput):
    """
    Datos de salida de la característica de traducción.

    Atributos:
        - translation: Texto traducido.
    """

    translation: str | None = None


class TranslateFeature(Feature[TranslateFeatureInput, TranslateFeatureOutput]):
    """
    Característica de traducción.

    Atributos:
        - languages_repository: Repositorio de idiomas.
    """

    languages_repository: LanguagesRepository

    @inject
    def __init__(self, languages_repository: LanguagesRepository):
        self.languages_repository = languages_repository

    def execute(self, input: TranslateFeatureInput) -> TranslateFeatureOutput:
        """
        Toma las entradas de traducción, ejecuta la traducción y devuelve la
        salida.
        """
        return TranslateFeatureOutput(translation=self.translate(**dict(input)))

    def translate(
        self,
        source: str,
        target: str,
        text: str,
        model: LanguageModel | None = None,
    ) -> str | None:
        """
        Traduce el texto de un idioma a otro, utilizando el modelo de
        traducción especificado, o el más adecuado, en su defecto.
        """
        if source == target:
            return text

        def translate(text: str | None, translator: Translator) -> str | None:
            if text is None:
                return None

            return translator.translate(text)

        translators = self.translators(source, target, model)
        return reduce(translate, translators, text)

    def translators(
        self,
        source: str,
        target: str,
        model: LanguageModel | None = None,
    ) -> Iterator[Translator]:
        """
        Devuelve los traductores que se deben utilizar para traducir el texto
        de un idioma a otro, utilizando el modelo de traducción especificado,
        o el más adecuado, en su defecto.
        """

        def translator(edge: Edge) -> Translator:
            """
            Obtiene el traductor según el modelo de traducción.
            """
            *codes, model = edge
            match model:
                case LanguageModel.ML:
                    return MLTranslator(*codes)
                case LanguageModel.CLOUD:
                    return CloudTranslator(*codes)

        injector = Injector()
        graph = injector.get(TranslationGraph)

        # Se obtiene la ruta de traducción que se debe seguir.
        path = graph.path(source, target, model)
        return map(translator, path)
