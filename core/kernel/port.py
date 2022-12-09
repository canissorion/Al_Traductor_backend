from abc import ABCMeta, abstractmethod
from typing import Generic, TypeVar
from core.kernel.feature.feature_input import FeatureInput
from core.kernel.feature.feature_output import FeatureOutput
from core.kernel.request import Request
from core.kernel.response import Response

TRequest = TypeVar("TRequest", bound=Request)
TResponse = TypeVar("TResponse", bound=Response)
TFeatureInput = TypeVar("TFeatureInput", bound=FeatureInput)
TFeatureOutput = TypeVar("TFeatureOutput", bound=FeatureOutput)


class Port(
    Generic[
        TRequest,
        TResponse,
        TFeatureInput,
        TFeatureOutput,
    ],
    metaclass=ABCMeta,
):
    """
    Clase base para un puerto.

    Un puerto es el componente que se encarga de adaptar los datos de la capa
    de interfaces y controladores a los de la capa de dominio y características.

    Parámetros genéricos:
        - TRequest: Tipo de la petición.
        - TResponse: Tipo de la respuesta.
        - TFeatureInput: Tipo de los datos de entrada de la característica.
        - TFeatureOutput: Tipo de los datos de salida de la característica.

    Métodos:
        - input: Convierte una petición en datos de entrada de una característica.
        - output: Convierte los datos de salida de una característica en una respuesta.
    """

    @abstractmethod
    def input(self, request: TRequest) -> TFeatureInput:
        pass

    @abstractmethod
    def output(self, output: TFeatureOutput) -> TResponse:
        pass
