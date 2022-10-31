from pydantic import BaseModel


class SpeechSynthesis(BaseModel):
    source: str
    text: str
    # TODO(davideliseo): Definir.
    speech: str | None = None
