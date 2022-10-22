from abc import ABCMeta, abstractmethod
from fastapi import FastAPI


class Controller(metaclass=ABCMeta):
    # TODO(davideliseo): Dependencia de capa externa.
    app: FastAPI

    def __init__(self, app: FastAPI) -> None:
        self.app = app

    @abstractmethod
    def register(self) -> None:
        pass
