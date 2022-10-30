from injector import inject
from core.domain.language.language import LanguageModel

from core.kernel.feature.feature import Feature
from core.kernel.feature.feature_input import FeatureInput
from core.kernel.feature.feature_output import FeatureOutput

from core.domain.language.repositories.languages_repository import LanguagesRepository
from core.domain.translation.repositories.translators.translator import Translator
from core.domain.translation.repositories.translators.ml_translator import MLTranslator
from core.domain.translation.repositories.translators.cloud_translator import (
    CloudTranslator,
)


class TranslateFeatureInput(FeatureInput):
    source_language_code: str
    target_language_code: str
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
        source_language_code: str,
        target_language_code: str,
        model: LanguageModel | None,
        text: str,
    ) -> str | None:
        if source_language_code == target_language_code:
            return text

        translator = self.get_translator(
            source_language_code,
            target_language_code,
            model,
        )

        return translator.translate(text)

    def get_translator(
        self,
        source_language_code: str,
        target_language_code: str,
        model: LanguageModel | None,
    ) -> Translator:
        codes = (source_language_code, target_language_code)
        match model:
            case LanguageModel.ML:
                return MLTranslator(*codes)
            case LanguageModel.CLOUD | None:
                return CloudTranslator(*codes)
