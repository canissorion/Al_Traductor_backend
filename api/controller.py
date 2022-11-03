from abc import ABCMeta, abstractmethod
from injector import inject
from fastapi import FastAPI


class Controller(metaclass=ABCMeta):
    """
    Clase base para un controlador.

    Atributos:
        - app: Aplicación FastAPI.

    Métodos:
        - register: Registra el controlador en la aplicación.

    TODO(davideliseo): Dependencia de capa externa.
    """

    app: FastAPI

    @inject
    def __init__(self, app: FastAPI) -> None:
        self.app = app

    @abstractmethod
    def register(self) -> None:
        pass
