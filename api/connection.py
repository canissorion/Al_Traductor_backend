import typing as t
from fastapi import FastAPI, types as ft
from pydantic import BaseModel


class ConnectionResponse(BaseModel):
    status: str


class ConnectionController:
    # FIXME(davideliseo): Dependencia de capa externa.
    app: FastAPI

    def __init__(self, app: FastAPI):
        self.app = app

    def register(self) -> ft.DecoratedCallable:
        def method() -> ConnectionResponse:
            return ConnectionResponse(status="OK")

        decorate = self.app.get("/connection", response_model=ConnectionResponse)
        return decorate(method)
