from typing import Generic
from abc import ABCMeta, abstractmethod

from core.kernel.port import TFeatureInput, TFeatureOutput


class Feature(Generic[TFeatureInput, TFeatureOutput], metaclass=ABCMeta):
    """
    Clase base para una característica.

    Parámetros genéricos:
        - TFeatureInput: Tipo de los datos de entrada de la característica.
        - TFeatureOutput: Tipo de los datos de salida de la característica.

    Métodos:
        - execute: Ejecuta la característica.
    """

    @abstractmethod
    def execute(self, input: TFeatureInput) -> TFeatureOutput:
        pass
