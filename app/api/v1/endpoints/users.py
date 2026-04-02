"""
Endpoints de la API para la gestión de usuarios.

Esta capa se encarga de:
- Recibir y validar requests HTTP
- Delegar la lógica de negocio a los servicios
- Retornar responses HTTP apropiadas
"""

from typing import Sequence

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db_session
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
async def create_user(
    user_data: UserCreate, db: AsyncSession = Depends(get_db_session)
) -> UserResponse:
    """
    Crea un nuevo usuario.

    Args:
        user_data: Datos del usuario a crear.
        db: Sesión de base de datos inyectada.

    Returns:
        El usuario creado.

    Raises:
        HTTPException: Si hay error de validación o recurso duplicado.
    """
    try:
        user = await user_service.create_user(db, user_data)
        return user
    except ApplicationException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Obtener usuario por ID",
    description="Recupera los datos de un usuario específico por su ID.",
)
async def get_user(
    user_id: int, db: AsyncSession = Depends(get_db_session)
) -> UserResponse:
    """
    Obtiene un usuario por su ID.

    Args:
        user_id: ID del usuario.
        db: Sesión de base de datos inyectada.

    Returns:
        El usuario encontrado.

    Raises:
        HTTPException: Si el usuario no existe.
    """
    try:
        user = await user_service.get_user_by_id(db, user_id)
        return user
    except ApplicationException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    summary="Actualizar usuario",
    description="Actualiza los datos de un usuario existente.",
)
async def update_user(
    user_id: int, user_data: UserUpdate, db: AsyncSession = Depends(get_db_session)
) -> UserResponse:
    """
    Actualiza un usuario existente.

    Args:
        user_id: ID del usuario a actualizar.
        user_data: Datos actualizados.
        db: Sesión de base de datos inyectada.

    Returns:
        El usuario actualizado.

    Raises:
        HTTPException: Si el usuario no existe o hay error de validación.
    """
    try:
        user = await user_service.update_user(db, user_id, user_data)
        return user
    except ApplicationException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)


@router.delete(
    "/{user_id}",
    response_model=UserResponse,
    summary="Eliminar usuario",
    description="Elimina permanentemente un usuario del sistema.",
)
async def delete_user(
    user_id: int, db: AsyncSession = Depends(get_db_session)
) -> UserResponse:
    """
    Elimina un usuario.

    Args:
        user_id: ID del usuario a eliminar.
        db: Sesión de base de datos inyectada.

    Returns:
        El usuario eliminado.

    Raises:
        HTTPException: Si el usuario no existe.
    """
    try:
        user = await user_service.delete_user(db, user_id)
        return user
    except ApplicationException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
