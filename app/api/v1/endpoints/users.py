"""
Endpoints de la API para la gestión de usuarios.

Esta capa se encarga de:
- Recibir y validar requests HTTP
- Delegar la lógica de negocio a los servicios
- Retornar responses HTTP apropiadas

Nota: Con MongoDB/Beanie, no es necesario inyectar la sesión de base de datos
como en SQLAlchemy, ya que Motor maneja las conexiones de forma async.
"""

from typing import Sequence

from fastapi import APIRouter, HTTPException, status

from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.services.user_service import user_service
from app.core.exceptions import ApplicationException

router = APIRouter()


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo usuario",
    description="Crea un nuevo usuario en el sistema con los datos proporcionados.",
)
async def create_user(user_data: UserCreate) -> UserResponse:
    """
    Crea un nuevo usuario.

    Args:
        user_data: Datos del usuario a crear.

    Returns:
        El usuario creado.

    Raises:
        HTTPException: Si hay error de validación o recurso duplicado.
    """
    try:
        user = await user_service.create_user(user_data)
        return user
    except ApplicationException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Obtener usuario por ID",
    description="Recupera los datos de un usuario específico por su ID.",
)
async def get_user(user_id: str) -> UserResponse:
    """
    Obtiene un usuario por su ID.

    Args:
        user_id: ID del usuario (string de ObjectId MongoDB).

    Returns:
        El usuario encontrado.

    Raises:
        HTTPException: Si el usuario no existe.
    """
    try:
        user = await user_service.get_user_by_id(user_id)
        return user
    except ApplicationException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    summary="Actualizar usuario",
    description="Actualiza los datos de un usuario existente.",
)
async def update_user(user_id: str, user_data: UserUpdate) -> UserResponse:
    """
    Actualiza un usuario existente.

    Args:
        user_id: ID del usuario a actualizar (string de ObjectId MongoDB).
        user_data: Datos actualizados del usuario.

    Returns:
        El usuario actualizado.

    Raises:
        HTTPException: Si el usuario no existe o hay error de validación.
    """
    try:
        user = await user_service.update_user(user_id, user_data)
        return user
    except ApplicationException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)


@router.delete(
    "/{user_id}",
    response_model=UserResponse,
    summary="Eliminar usuario",
    description="Elimina permanentemente un usuario del sistema.",
)
async def delete_user(user_id: str) -> UserResponse:
    """
    Elimina un usuario.

    Args:
        user_id: ID del usuario a eliminar (string de ObjectId MongoDB).

    Returns:
        El usuario eliminado.

    Raises:
        HTTPException: Si el usuario no existe.
    """
    try:
        user = await user_service.delete_user(user_id)
        return user
    except ApplicationException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
