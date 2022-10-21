from pydantic import BaseModel


class SpeechSynthesis(BaseModel):
    language_code: str
    text: str
    # TODO(davideliseo): Definir.
    speech: str | None = None
