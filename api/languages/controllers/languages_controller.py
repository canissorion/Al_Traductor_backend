from fastapi import FastAPI
from injector import inject

from api.controller import Controller
from api.languages.adapters.languages_response import LanguagesResponse
from core.language.repositories.languages_repository import LanguagesRepository


class LanguagesController(Controller):
    languages_repository: LanguagesRepository

    @inject
    def __init__(self, app: FastAPI, languages_repository: LanguagesRepository):
        self.languages_repository = languages_repository
        super().__init__(app)

    def register(self) -> None:
        @self.app.get("/languages", response_model=LanguagesResponse)
        def get() -> LanguagesResponse:
            languages = self.languages_repository.get_languages()
            return LanguagesResponse(languages=languages)
