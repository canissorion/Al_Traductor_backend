from abc import ABCMeta, abstractmethod


class Translator(metaclass=ABCMeta):
    source_language_code: str
    target_language_code: str

    def __init__(self, source_language_code: str, target_language_code: str) -> None:
        self.source_language_code = source_language_code
        self.target_language_code = target_language_code

    @abstractmethod
    def translate(self, text: str) -> str | None:
        pass
