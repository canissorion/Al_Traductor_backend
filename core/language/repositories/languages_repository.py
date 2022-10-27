from typing import Iterator
from core.language.language import Language, LanguageModel
from infrastructure.storage.yaml import YAMLStorage


# TODO(davideliseo): Convertir a singleton.
class LanguagesRepository:
    filename = "core/language/repositories/sources/languages_source.yaml"
    storage = YAMLStorage(filename=filename)

    def get_languages(self) -> Iterator[Language] | None:
        if (languages := self.storage.read()) is None:
            return None

        return (Language(code=code, **language) for code, language in languages.items())

    def get_ml_languages(self) -> Iterator[Language] | None:
        if (languages := self.get_languages()) is None:
            return None

        def filter_by_ml(language: Language) -> bool:
            return language.model == LanguageModel.ML

        return filter(filter_by_ml, languages)

    def get_api_languages(self) -> Iterator[Language] | None:
        if (languages := self.get_languages()) is None:
            return None

        def filter_by_cloud(language: Language) -> bool:
            return language.model == LanguageModel.CLOUD

        return filter(filter_by_cloud, languages)
