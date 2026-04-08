"""
Repositorio específico para la entidad Usuario en MongoDB.

Extiende el repositorio base con operaciones específicas
para la gestión de usuarios usando Beanie ODM.
"""

from app.models.user import UserDocument
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[UserDocument]):
    """
    Repositorio para operaciones de acceso a datos de usuarios.

    Utiliza Beanie ODM para interactuar con MongoDB de manera asíncrona.
    """

    def __init__(self):
        super().__init__(UserDocument)

    async def get_by_email(self, email: str) -> UserDocument | None:
        """
        Busca un usuario por su correo electrónico.

        Args:
            email: Correo electrónico del usuario.

        Returns:
            El usuario si existe, None en caso contrario.
        """
        return await self._document_model.find_one(UserDocument.email == email)

    async def get_by_username(self, username: str) -> UserDocument | None:
        """
        Busca un usuario por su nombre de usuario.

        Args:
            username: Nombre de usuario.

        Returns:
            El usuario si existe, None en caso contrario.
        """
        return await self._document_model.find_one(UserDocument.username == username)

    async def email_exists(self, email: str) -> bool:
        """
        Verifica si un correo electrónico ya está registrado.

        Args:
            email: Correo electrónico a verificar.

        Returns:
            True si el email existe, False en caso contrario.
        """
        user = await self.get_by_email(email)
        return user is not None

    async def username_exists(self, username: str) -> bool:
        """
        Verifica si un nombre de usuario ya está registrado.

        Args:
            username: Nombre de usuario a verificar.

        Returns:
            True si el username existe, False en caso contrario.
        """
        user = await self.get_by_username(username)
        return user is not None


# Instancia singleton del repositorio
user_repository = UserRepository()
