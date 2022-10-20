from core.language.entity import Language
from infrastructure.storage.yaml import YAMLStorage


class LanguagesRepository:
    def get_languages(self) -> list[Language]:
        storage = YAMLStorage(filename="infrastructure/sources/languages.yaml")
        languages: dict | None = storage.read()
        return [Language(code=code, **language) for code, language in languages.items()]
