from abc import ABCMeta, abstractmethod
from typing import Generic, TypeVar
from pydantic import BaseModel


class ValidationData(BaseModel, metaclass=ABCMeta):
    """
    Clase base para datos de validación.
    """

    pass


TValidationData = TypeVar("TValidationData", bound=ValidationData)


class Validator(Generic[TValidationData], metaclass=ABCMeta):
    """
    Clase base para un validador.

    Parámetros genéricos:
        - TValidationData: Tipo de los datos de validación.

    Métodos:
        - validate: Valida los datos.
    """

    @abstractmethod
    def validate(self, data: TValidationData) -> None:
        pass


class ValidationError(Exception):
    """
    Excepción para errores de validación.
    """

    pass
