from pydantic import BaseModel

from api.controller import Controller


class ConnectionResponse(BaseModel):
    status: str


class ConnectionController(Controller):
    def register(self) -> None:
        @self.app.get("/connection", response_model=ConnectionResponse)
        def method() -> ConnectionResponse:
            return ConnectionResponse(status="OK")
