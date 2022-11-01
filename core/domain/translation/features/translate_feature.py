import functools
from typing import Iterator
from injector import inject, Injector

from core.kernel.feature.feature import Feature
from core.kernel.feature.feature_input import FeatureInput
from core.kernel.feature.feature_output import FeatureOutput

from core.domain.language.language import LanguageModel
from core.domain.language.languages_graph import Edge, LanguagesGraph

from core.domain.language.repositories.languages_repository import LanguagesRepository
from core.domain.translation.repositories.translators.translator import Translator
from core.domain.translation.repositories.translators.ml_translator import MLTranslator
from core.domain.translation.repositories.translators.cloud_translator import (
    CloudTranslator,
)


class TranslateFeatureInput(FeatureInput):
    source: str
    target: str
    model: LanguageModel | None = None
    text: str


class TranslateFeatureOutput(FeatureOutput):
    pass


class TranslateFeature(Feature[TranslateFeatureInput, TranslateFeatureOutput]):
    languages_repository: LanguagesRepository

    @inject
    def __init__(self, languages_repository: LanguagesRepository):
        self.languages_repository = languages_repository

    def execute(self, input: TranslateFeatureInput) -> TranslateFeatureOutput:
        return TranslateFeatureOutput(value=self.translate(**dict(input)))

    def translate(
        self,
        source: str,
        target: str,
        model: LanguageModel | None,
        text: str,
    ) -> str | None:
        if source == target:
            return text

        def translate(text: str | None, translator: Translator) -> str | None:
            if text is None:
                return None

            return translator.translate(text)

        translators = list(self.translators(source, target, model))
        print(translators)
        return functools.reduce(translate, translators, text)

    def translators(
        self,
        source: str,
        target: str,
        model: LanguageModel | None,
    ) -> Iterator[Translator]:
        def translator(edge: Edge) -> Translator:
            source, target, model = edge
            match model:
                case LanguageModel.ML:
                    return MLTranslator(source, target)
                case LanguageModel.CLOUD:
                    return CloudTranslator(source, target)

        injector = Injector()
        graph = injector.get(LanguagesGraph)
        path = graph.path(source, target, model)
        return map(translator, path)
