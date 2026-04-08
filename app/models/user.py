"""
Modelo de documento para la entidad Usuario en MongoDB.

Utiliza Beanie como ODM (Object Document Mapper) para MongoDB,
que es similar a SQLAlchemy pero para documentos NoSQL.
"""

from datetime import datetime
from typing import Optional

from beanie import Document, Indexed
from pydantic import Field, EmailStr


class UserDocument(Document):
    """
    Documento MongoDB que representa un usuario en el sistema.

    Attributes:
        email: Correo electrónico único del usuario.
        username: Nombre de usuario único.
        hashed_password: Contraseña hasheada para autenticación.
        is_active: Indica si el usuario está activo.
        is_superuser: Indica si el usuario tiene privilegios de administrador.
        created_at: Fecha de creación del registro.
        updated_at: Fecha de última actualización.
    """

    email: Indexed(EmailStr, unique=True)  # type: ignore[valid-type]
    username: Indexed(str, unique=True)  # type: ignore[valid-type]
    hashed_password: str
    is_active: bool = True
    is_superuser: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        """Configuración del documento en MongoDB."""

        name = "users"  # Nombre de la colección

    class Config:
        """Configuración del modelo Pydantic."""

        json_encoders = {datetime: lambda v: v.isoformat()}

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email}, username={self.username})>"

    async def update_timestamp(self) -> None:
        """
        Actualiza el campo updated_at a la fecha/hora actual.
        """
        self.updated_at = datetime.utcnow()
        await self.save()
