from typing import Callable, Iterator
from core.domain.language.language import Language, LanguageModel
from infrastructure.storage.yaml import YAMLStorage


# TODO(davideliseo): Convertir a singleton.
class LanguagesRepository:
    filename = "core/domain/language/repositories/sources/languages_source.yaml"
    storage = YAMLStorage(filename=filename)

    def all(self) -> Iterator[Language]:
        if (languages := self.storage.read()) is None:
            return iter(())

        return (Language(code=code, **language) for code, language in languages.items())

    def query(self, models: set[LanguageModel]) -> Iterator[Language]:
        return self.filter(lambda language: models <= set(language.models))

    def filter(
        self,
        filter_by: Callable[[Language], bool],
    ) -> Iterator[Language]:
        return filter(filter_by, self.all())
