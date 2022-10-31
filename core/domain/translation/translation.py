from pydantic import BaseModel


class Translation(BaseModel):
    source: str
    target: str
    text: str
    translation: str | None = None
