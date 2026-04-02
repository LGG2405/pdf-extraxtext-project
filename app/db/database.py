"""
Configuración de la base de datos y gestión de sesiones.
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

from app.core.config import get_settings

settings = get_settings()

# Base para los modelos ORM
Base = declarative_base()

# Motor de base de datos asíncrono
engine = create_async_engine(settings.DATABASE_URL, echo=False, future=True)

# Factory de sesiones asíncronas
AsyncSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def get_db_session():
    """
    Generador de sesiones de base de datos para dependency injection.

    Yields:
        AsyncSession: Sesión de base de datos activa.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def create_tables():
    """
    Crea todas las tablas definidas en los modelos.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
