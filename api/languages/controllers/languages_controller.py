from api.controller import Controller

from api.languages.adapters.languages_response import LanguagesResponse
from core.language.repositories.languages_repository import LanguagesRepository


class LanguagesController(Controller):
    def register(self) -> None:
        @self.app.get("/languages", response_model=LanguagesResponse)
        def get() -> LanguagesResponse:
            repository = LanguagesRepository()
            languages = repository.get_languages()
            return LanguagesResponse(languages=languages)
