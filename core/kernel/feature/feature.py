from typing import Generic
from abc import ABCMeta, abstractmethod

from core.kernel.port import TFeatureInput, TFeatureOutput


class Feature(Generic[TFeatureInput, TFeatureOutput], metaclass=ABCMeta):
    @abstractmethod
    def execute(self, input: TFeatureInput) -> TFeatureOutput:
        pass
