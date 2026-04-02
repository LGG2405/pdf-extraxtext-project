"""
Configuración centralizada de la aplicación.

Utiliza Pydantic Settings para la gestión de configuraciones
con validación de tipos y valores por defecto.
"""

from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Configuraciones de la aplicación cargadas desde variables de entorno.
    """

    # Información del proyecto
    PROJECT_NAME: str = "FastAPI Clean Architecture"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "API con arquitectura de tres capas y Clean Code"

    # Configuración de la API
    API_V1_STR: str = "/api/v1"

    # Configuración de base de datos
    DATABASE_URL: str = "sqlite:///./app.db"

    # Configuración de seguridad
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"

    # Configuración de logging
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """
    Retorna una instancia cacheada de la configuración.

    El cacheo evita múltiples lecturas del archivo .env
    y mejora el rendimiento.

    Returns:
        Settings: Instancia de configuración de la aplicación.
    """
    return Settings()
