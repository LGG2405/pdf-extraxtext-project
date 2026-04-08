"""
Punto de entrada principal de la aplicación FastAPI con MongoDB.
"""

from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.api.v1.router import api_router
from app.core.config import get_settings
from app.core.logging import configure_logging
from app.db.database import init_database, close_database


settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gestor del ciclo de vida de la aplicación.
    Se ejecuta al iniciar y al cerrar la aplicación.

    Inicializa la conexión a MongoDB y configura Beanie ODM.
    """
    configure_logging()
    await init_database()
    yield
    await close_database()


def create_application() -> FastAPI:
    """
    Factory para crear la instancia de la aplicación FastAPI.

    Returns:
        FastAPI: Instancia configurada de la aplicación.
    """
    application = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        description=settings.DESCRIPTION,
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )

    application.include_router(api_router, prefix=settings.API_V1_STR)

    return application


app = create_application()


@app.get("/health")
async def health_check():
    """
    Endpoint de verificación de salud del sistema.
    """
    return {"status": "healthy"}
