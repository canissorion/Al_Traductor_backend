from core.language.repository.languages import LanguagesRepository
from core.translation.translators.cloud_translator import CloudTranslator
from core.translation.translators.ml_translator import MLTranslator
from core.translation.translators.translator import Translator


class TranslateFeature:
    languages_repository: LanguagesRepository

    def __init__(self, languages_repository: LanguagesRepository):
        self.languages_repository = languages_repository

    def __call__(
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
        self, source_language_code: str, target_language_code: str
    ) -> Translator:
        codes = (source_language_code, target_language_code)
        ml_languages = self.languages_repository.get_ml_languages()
        ml_codes = (language.code for language in ml_languages)

        # Si ninguno de los dos idiomas es de tipo ML, se usa el traductor Cloud.
        if set(ml_codes).isdisjoint(codes):
            return CloudTranslator(*codes)

        return MLTranslator(*codes)
