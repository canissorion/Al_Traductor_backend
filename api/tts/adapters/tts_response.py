from pydantic import BaseModel


# TODO(davideliseo): Definir.
class TTSResponse(BaseModel):
    speech: str | None = None
