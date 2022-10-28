from typing import Any
from pydantic import BaseModel


class FeatureOutput(BaseModel):
    value: Any | None = None
