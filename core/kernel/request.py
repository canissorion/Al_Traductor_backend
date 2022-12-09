from abc import ABCMeta
from pydantic import BaseModel


class Request(BaseModel, metaclass=ABCMeta):
    """
    Clase base para una petición de un controlador.
    """

    pass
