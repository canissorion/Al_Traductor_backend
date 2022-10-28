from typing import Callable, Iterator
from core.domain.language.language import Language, LanguageModel
from infrastructure.storage.yaml import YAMLStorage


# TODO(davideliseo): Convertir a singleton.
class LanguagesRepository:
    filename = "core/domain/language/repositories/sources/languages_source.yaml"
    storage = YAMLStorage(filename=filename)

    def get_languages(self) -> Iterator[Language] | None:
        if (languages := self.storage.read()) is None:
            return None

        return (Language(code=code, **language) for code, language in languages.items())

    def get_ml_languages(self) -> Iterator[Language] | None:
        return self.filter(lambda language: LanguageModel.ML in language.models)

    def get_cloud_languages(self) -> Iterator[Language] | None:
        return self.filter(lambda language: LanguageModel.CLOUD in language.models)

    def filter(
        self,
        filter_by: Callable[[Language], bool],
    ) -> Iterator[Language] | None:
        if (languages := self.get_languages()) is None:
            return None

        return filter(filter_by, languages)
