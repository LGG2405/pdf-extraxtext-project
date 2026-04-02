"""
Schemas Pydantic para la entidad Usuario.

Estos schemas definen la estructura de datos para:
- Validación de entrada
- Serialización de salida
- Documentación automática de la API
"""

from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict


class UserBase(BaseModel):
    """
    Campos base compartidos por todos los schemas de usuario.
    """

    email: EmailStr
    username: str
    is_active: bool = True


class UserCreate(UserBase):
    """
    Schema para la creación de un nuevo usuario.

    Attributes:
        password: Contraseña en texto plano (será hasheada antes de almacenar).
    """

    password: str


class UserUpdate(BaseModel):
    """
    Schema para la actualización de un usuario existente.

    Todos los campos son opcionales para permitir actualizaciones parciales.
    """

    email: EmailStr | None = None
    username: str | None = None
    password: str | None = None
    is_active: bool | None = None


class UserResponse(UserBase):
    """
    Schema para la respuesta de un usuario.

    Excluye campos sensibles como la contraseña hasheada.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    is_superuser: bool
    created_at: datetime
    updated_at: datetime


class UserInDB(UserBase):
    """
    Schema interno que incluye la contraseña hasheada.

    Este schema nunca debe ser expuesto en las respuestas de la API.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    hashed_password: str
    is_superuser: bool
    created_at: datetime
    updated_at: datetime
