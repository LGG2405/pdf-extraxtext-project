"""
Servicio de negocio para la gestión de usuarios.

Esta clase encapsula la lógica de negocio relacionada con usuarios,
desacoplando la capa de API de los detalles de implementación.
"""

from datetime import datetime

from passlib.context import CryptContext

from app.core.exceptions import (
    ResourceNotFoundException,
    DuplicateResourceException,
    ValidationException,
)
from app.models.user import UserDocument
from app.repositories.user_repository import user_repository
from app.schemas.user import UserCreate, UserUpdate


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    """
    Servicio que gestiona la lógica de negocio de usuarios.

    Esta clase actúa como intermediario entre los endpoints de la API
    y el repositorio de datos, aplicando reglas de negocio y validaciones.

    Nota: Con Beanie/MongoDB, no necesitamos manejar sesiones explícitamente
    como en SQLAlchemy, ya que Motor maneja las conexiones de forma async.
    """

    def __init__(self):
        self._repository = user_repository

    def _hash_password(self, password: str) -> str:
        """
        Genera un hash seguro de la contraseña.

        Args:
            password: Contraseña en texto plano.

        Returns:
            Hash bcrypt de la contraseña.
        """
        return pwd_context.hash(password)

    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verifica si una contraseña coincide con su hash.

        Args:
            plain_password: Contraseña en texto plano.
            hashed_password: Hash almacenado de la contraseña.

        Returns:
            True si la contraseña es válida, False en caso contrario.
        """
        return pwd_context.verify(plain_password, hashed_password)

    async def create_user(self, user_data: UserCreate) -> UserDocument:
        """
        Crea un nuevo usuario en el sistema.

        Args:
            user_data: Datos del usuario a crear.

        Returns:
            El usuario creado.

        Raises:
            DuplicateResourceException: Si el email o username ya existen.
            ValidationException: Si la contraseña es demasiado corta.
        """
        if len(user_data.password) < 6:
            raise ValidationException("La contraseña debe tener al menos 6 caracteres")

        if await self._repository.email_exists(user_data.email):
            raise DuplicateResourceException("Usuario", "email", user_data.email)

        if await self._repository.username_exists(user_data.username):
            raise DuplicateResourceException("Usuario", "username", user_data.username)

        user_dict = user_data.model_dump()
        user_dict["hashed_password"] = self._hash_password(user_dict.pop("password"))
        user_dict["created_at"] = datetime.utcnow()
        user_dict["updated_at"] = datetime.utcnow()

        return await self._repository.create(user_dict)

    async def get_user_by_id(self, user_id: str) -> UserDocument:
        """
        Obtiene un usuario por su ID.

        Args:
            user_id: ID del usuario (string de ObjectId).

        Returns:
            El usuario encontrado.

        Raises:
            ResourceNotFoundException: Si el usuario no existe.
        """
        user = await self._repository.get_by_id(user_id)
        if not user:
            raise ResourceNotFoundException("Usuario", user_id)
        return user

    async def get_user_by_email(self, email: str) -> UserDocument | None:
        """
        Busca un usuario por su email.

        Args:
            email: Email del usuario.

        Returns:
            El usuario si existe, None en caso contrario.
        """
        return await self._repository.get_by_email(email)

    async def update_user(self, user_id: str, user_data: UserUpdate) -> UserDocument:
        """
        Actualiza los datos de un usuario existente.

        Args:
            user_id: ID del usuario a actualizar (string de ObjectId).
            user_data: Datos actualizados del usuario.

        Returns:
            El usuario actualizado.

        Raises:
            ResourceNotFoundException: Si el usuario no existe.
            DuplicateResourceException: Si el nuevo email ya está en uso.
        """
        user = await self.get_user_by_id(user_id)

        update_data = user_data.model_dump(exclude_unset=True)

        # Verificar email duplicado
        if "email" in update_data and update_data["email"] != user.email:
            if await self._repository.email_exists(update_data["email"]):
                raise DuplicateResourceException("Usuario", "email", update_data["email"])

        # Hashear nueva contraseña si se proporciona
        if "password" in update_data:
            if len(update_data["password"]) < 6:
                raise ValidationException("La contraseña debe tener al menos 6 caracteres")
            update_data["hashed_password"] = self._hash_password(update_data.pop("password"))

        # Actualizar timestamp
        update_data["updated_at"] = datetime.utcnow()

        return await self._repository.update(user, update_data)

    async def delete_user(self, user_id: str) -> UserDocument:
        """
        Elimina un usuario del sistema.

        Args:
            user_id: ID del usuario a eliminar (string de ObjectId).

        Returns:
            El usuario eliminado.

        Raises:
            ResourceNotFoundException: Si el usuario no existe.
        """
        user = await self.get_user_by_id(user_id)
        await self._repository.delete(user)
        return user


# Instancia singleton del servicio
user_service = UserService()
