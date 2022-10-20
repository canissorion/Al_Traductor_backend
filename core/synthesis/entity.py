from pydantic import BaseModel


class Synthesis(BaseModel):
    language_code: str
    text: str
    # TODO(davideliseo): Definir.
    speech: str | None = None
