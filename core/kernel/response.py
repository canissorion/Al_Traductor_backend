from abc import ABCMeta
from pydantic import BaseModel


class Response(BaseModel, metaclass=ABCMeta):
    pass
