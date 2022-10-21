from core.language.entity import Language, LanguageModel
from infrastructure.storage.yaml import YAMLStorage


# TODO(davideliseo): Convertir a singleton.
class LanguagesRepository:
    storage = YAMLStorage(filename="infrastructure/sources/languages.yaml")

    def get_languages(self) -> list[Language] | None:
        if (languages := self.storage.read()) is None:
            return None

        return [Language(code=code, **language) for code, language in languages.items()]

    def get_ml_languages(self) -> list[Language] | None:
        languages = self.get_languages()

        def filter_by_ml(language: Language) -> bool:
            return language.model == LanguageModel.ML

        return list(filter(filter_by_ml, languages))

    def get_api_languages(self) -> list[Language] | None:
        languages = self.get_languages()

        def filter_by_api(language: Language) -> bool:
            return language.model == LanguageModel.API

        return list(filter(filter_by_api, languages))
