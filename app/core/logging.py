"""
Configuración de logging estructurado para la aplicación.
"""

import logging
import sys

from app.core.config import get_settings


def configure_logging():
    """
    Configura el sistema de logging de la aplicación.

    Establece el nivel de logging y el formato de los mensajes.
    """
    settings = get_settings()

    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )

    # Reducir ruido de logs de librerías externas
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
