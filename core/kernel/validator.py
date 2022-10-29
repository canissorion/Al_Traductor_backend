from abc import ABCMeta, abstractmethod
from typing import Generic, TypeVar
from pydantic import BaseModel


class ValidationData(BaseModel):
    pass


TValidationData = TypeVar("TValidationData", bound=ValidationData)


class Validator(Generic[TValidationData], metaclass=ABCMeta):
    @abstractmethod
    def validate(self, data: TValidationData) -> None:
        pass


class ValidationError(Exception):
    pass
