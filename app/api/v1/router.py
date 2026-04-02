"""
Router principal de la API v1.

Agrupa todos los routers de endpoints de la versión 1 de la API.
"""

from fastapi import APIRouter

from app.api.v1.endpoints import users

api_router = APIRouter()

api_router.include_router(users.router, prefix="/users", tags=["users"])
