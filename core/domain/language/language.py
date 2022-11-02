from __future__ import annotations
from enum import Enum, unique
from pydantic import BaseModel
import functools


@unique
class LanguageModel(str, Enum):
    ML = "ml"
    CLOUD = "cloud"

    @staticmethod
    @functools.cache
    def precedence(model: LanguageModel) -> int:
        precedence = {LanguageModel.ML: 0, LanguageModel.CLOUD: 1}
        return precedence[model]


@unique
class LanguageFeature(str, Enum):
    TRANSLATE = "translate"
    TTS = "tts"


@unique
class LanguageSupportMode(str, Enum):
    INCLUDE = "include"
    EXCLUDE = "exclude"


class LanguageSupport(BaseModel):
    mode: LanguageSupportMode = LanguageSupportMode.EXCLUDE
    targets: set[str] = set()


class LanguageModelSettings(BaseModel):
    features: set[LanguageFeature] = set()
    support: LanguageSupport = LanguageSupport()

    def includes(self, target: str) -> bool:
        match self.support.mode:
            case LanguageSupportMode.EXCLUDE:
                return target not in self.support.targets
            case LanguageSupportMode.INCLUDE:
                return target in self.support.targets


class Language(BaseModel):
    name: str
    code: str
    models: dict[LanguageModel, LanguageModelSettings] = dict()
