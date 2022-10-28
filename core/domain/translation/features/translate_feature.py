from injector import inject

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
    text: str


class TranslateFeatureOutput(FeatureOutput):
    pass


class TranslateFeature(Feature[TranslateFeatureInput, TranslateFeatureOutput]):
    languages_repository: LanguagesRepository

    @inject
    def __init__(self, languages_repository: LanguagesRepository):
        self.languages_repository = languages_repository

    def execute(self, input: TranslateFeatureInput) -> TranslateFeatureOutput:
        return TranslateFeatureOutput(value=self.translate(*input.dict().values()))

    def translate(
        self,
        source_language_code: str,
        target_language_code: str,
        text: str,
    ) -> str | None:
        if source_language_code == target_language_code:
            return text

        translator = self.get_translator(source_language_code, target_language_code)
        return translator.translate(text)

    def get_translator(
        self,
        source_language_code: str,
        target_language_code: str,
    ) -> Translator:
        # Se usa el traductor ML sólo si los dos idiomas son ML.
        if self.all_ml_languages(codes := {source_language_code, target_language_code}):
            return MLTranslator(*codes)

        return CloudTranslator(*codes)

    def all_ml_languages(self, codes: set[str]) -> bool:
        if (ml_languages := self.languages_repository.get_ml_languages()) is None:
            return False

        # Se comprueba que los códigos sean un subconjunto de los idiomas ML.
        return codes <= {language.code for language in ml_languages}
