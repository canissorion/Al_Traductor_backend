from enum import Enum, unique
from functools import lru_cache
from pydantic import BaseSettings


@unique
class AppEnv(str, Enum):
    """
    Tipo de entorno de la aplicación.
    """

    DEVELOPMENT = "development"
    PRODUCTION = "production"


class Settings(BaseSettings):
    """
    Configuración de la aplicación.

    Attributes:
        - app_env: Tipo de entorno de la aplicación.
    """

    app_env: str = AppEnv.DEVELOPMENT

    class Config:  # pyright: ignore
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """
    Obtiene la configuración de la aplicación.
    """
    return Settings()
