from pydantic import BaseModel

from api.controller import Controller


class ConnectionResponse(BaseModel):
    """
    Respuesta de la API con el estado de la conexión.

    Atributos:
        - status: Estado de la conexión.
    """

    status: str


class ConnectionController(Controller):
    """
    Controlador de la API para comprueba la conexión con el servidor.

    Atributos:
        - app: Aplicación FastAPI.
    """

    def register(self) -> None:
        """
        Registra el endpoint para comprobar la conexión con el servidor.
        """

        @self.app.get("/connection", response_model=ConnectionResponse)
        def _() -> ConnectionResponse:
            return ConnectionResponse(status="OK")
