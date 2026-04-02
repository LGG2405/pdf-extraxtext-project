"""
Repositorio específico para la entidad Usuario.

Extiende el repositorio base con operaciones específicas
para la gestión de usuarios.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    """
    Repositorio para operaciones de acceso a datos de usuarios.
    """

    def __init__(self):
        super().__init__(User)

    async def get_by_email(self, db: AsyncSession, email: str) -> User | None:
        """
        Busca un usuario por su correo electrónico.

        Args:
            db: Sesión de base de datos.
            email: Correo electrónico del usuario.

        Returns:
            El usuario si existe, None en caso contrario.
        """
        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def get_by_username(self, db: AsyncSession, username: str) -> User | None:
        """
        Busca un usuario por su nombre de usuario.

        Args:
            db: Sesión de base de datos.
            username: Nombre de usuario.

        Returns:
            El usuario si existe, None en caso contrario.
        """
        result = await db.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    async def email_exists(self, db: AsyncSession, email: str) -> bool:
        """
        Verifica si un correo electrónico ya está registrado.

        Args:
            db: Sesión de base de datos.
            email: Correo electrónico a verificar.

        Returns:
            True si el email existe, False en caso contrario.
        """
        user = await self.get_by_email(db, email)
        return user is not None

    async def username_exists(self, db: AsyncSession, username: str) -> bool:
        """
        Verifica si un nombre de usuario ya está registrado.

        Args:
            db: Sesión de base de datos.
            username: Nombre de usuario a verificar.

        Returns:
            True si el username existe, False en caso contrario.
        """
        user = await self.get_by_username(db, username)
        return user is not None


# Instancia singleton del repositorio
user_repository = UserRepository()
