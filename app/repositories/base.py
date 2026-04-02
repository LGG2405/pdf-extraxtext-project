"""
Repositorio base abstracto que define las operaciones CRUD estándar.

Implementa el patrón Repository para desacoplar la capa de datos
de la lógica de negocio.
"""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.database import Base


ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(ABC, Generic[ModelType]):
    """
    Repositorio base que proporciona operaciones CRUD genéricas.

    Type Parameters:
        ModelType: El tipo del modelo ORM que maneja este repositorio.
    """

    def __init__(self, model: type[ModelType]):
        """
        Inicializa el repositorio con el modelo ORM correspondiente.

        Args:
            model: La clase del modelo ORM.
        """
        self._model = model

    async def get_by_id(self, db: AsyncSession, id: int) -> ModelType | None:
        """
        Obtiene un registro por su ID.

        Args:
            db: Sesión de base de datos.
            id: Identificador del registro.

        Returns:
            La instancia del modelo si existe, None en caso contrario.
        """
        result = await db.execute(select(self._model).where(self._model.id == id))
        return result.scalar_one_or_none()

    async def get_all(
        self, db: AsyncSession, skip: int = 0, limit: int = 100
    ) -> Sequence[ModelType]:
        """
        Obtiene una lista paginada de registros.

        Args:
            db: Sesión de base de datos.
            skip: Número de registros a omitir (offset).
            limit: Número máximo de registros a retornar.

        Returns:
            Lista de instancias del modelo.
        """
        result = await db.execute(select(self._model).offset(skip).limit(limit))
        return result.scalars().all()

    async def create(self, db: AsyncSession, obj_in: dict) -> ModelType:
        """
        Crea un nuevo registro en la base de datos.

        Args:
            db: Sesión de base de datos.
            obj_in: Diccionario con los datos a insertar.

        Returns:
            La instancia creada del modelo.
        """
        db_obj = self._model(**obj_in)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
        self, db: AsyncSession, db_obj: ModelType, obj_in: dict
    ) -> ModelType:
        """
        Actualiza un registro existente.

        Args:
            db: Sesión de base de datos.
            db_obj: Instancia del modelo a actualizar.
            obj_in: Diccionario con los datos a actualizar.

        Returns:
            La instancia actualizada del modelo.
        """
        for field, value in obj_in.items():
            if value is not None:
                setattr(db_obj, field, value)

        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: AsyncSession, id: int) -> ModelType | None:
        """
        Elimina un registro por su ID.

        Args:
            db: Sesión de base de datos.
            id: Identificador del registro a eliminar.

        Returns:
            La instancia eliminada si existía, None en caso contrario.
        """
        obj = await self.get_by_id(db, id)
        if obj:
            await db.delete(obj)
            await db.commit()
        return obj
