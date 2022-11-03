from abc import ABCMeta
from pydantic import BaseModel


class Response(BaseModel, metaclass=ABCMeta):
    """
    Clase base para una respuesta de un controlador.
    """

    pass
