from abc import ABCMeta, abstractmethod


class Translator(metaclass=ABCMeta):
    """
    Clase base para los traductores.

    Atributos:
        - source: Idioma de origen.
        - target: Idioma de destino.

    Métodos:
        - translate: Traduce el texto de un idioma a otro.
    """

    source: str
    target: str

    def __init__(self, source: str, target: str) -> None:
        self.source = source
        self.target = target

    @abstractmethod
    def translate(self, text: str) -> str | None:
        pass

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.source}, {self.target})"
