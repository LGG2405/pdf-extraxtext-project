"""
Modelo de dominio para la entidad Usuario.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime

from app.db.database import Base


class User(Base):
    """
    Modelo ORM que representa un usuario en el sistema.

    Attributes:
        id: Identificador único del usuario.
        email: Correo electrónico único del usuario.
        username: Nombre de usuario único.
        hashed_password: Contraseña hasheada para autenticación.
        is_active: Indica si el usuario está activo.
        is_superuser: Indica si el usuario tiene privilegios de administrador.
        created_at: Fecha de creación del registro.
        updated_at: Fecha de última actualización.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email}, username={self.username})>"
