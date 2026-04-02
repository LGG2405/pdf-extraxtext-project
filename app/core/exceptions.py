"""
Excepciones personalizadas del dominio de la aplicación.

Estas excepciones permiten un manejo de errores más granular
y semántico en toda la aplicación.
"""


class ApplicationException(Exception):
    """
    Excepción base para errores de la aplicación.

    Attributes:
        message: Mensaje descriptivo del error.
        status_code: Código HTTP asociado al error.
    """

    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class ResourceNotFoundException(ApplicationException):
    """
    Excepción lanzada cuando un recurso no es encontrado.
    """

    def __init__(self, resource_name: str, resource_id: str):
        message = f"{resource_name} con id '{resource_id}' no encontrado"
        super().__init__(message, status_code=404)


class ValidationException(ApplicationException):
    """
    Excepción lanzada cuando los datos de entrada no son válidos.
    """

    def __init__(self, message: str):
        super().__init__(message, status_code=422)


class DuplicateResourceException(ApplicationException):
    """
    Excepción lanzada cuando se intenta crear un recurso duplicado.
    """

    def __init__(self, resource_name: str, field: str, value: str):
        message = f"{resource_name} con {field} '{value}' ya existe"
        super().__init__(message, status_code=409)
