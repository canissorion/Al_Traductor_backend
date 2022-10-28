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
    @abstractmethod
    def input(self, request: TRequest) -> TFeatureInput:
        pass

    @abstractmethod
    def output(self, output: TFeatureOutput) -> TResponse:
        pass
