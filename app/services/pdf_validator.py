"""Servicio de validación de archivos PDF.

Este módulo implementa las 7 validaciones requeridas:
1. Existe el archivo
2. Pesa más de 0 KB
3. Extensión .pdf
4. Header %PDF-
5. No está cifrado
6. Tiene páginas
7. Tiene texto extraíble
"""

from typing import Any


def validate_file_exists(file: Any) -> bool:
    """Valida que el archivo exista y tenga nombre."""
    raise NotImplementedError("FASE ROJA: Implementar validación de existencia")


def validate_file_size(content: bytes) -> bool:
    """Valida que el archivo tenga contenido (> 0 bytes)."""
    raise NotImplementedError("FASE ROJA: Implementar validación de tamaño")


def validate_file_extension(filename: str) -> bool:
    """Valida que la extensión sea .pdf (case-insensitive)."""
    raise NotImplementedError("FASE ROJA: Implementar validación de extensión")


def validate_pdf_header(content: bytes) -> bool:
    """Valida que el header binario sea %PDF-."""
    raise NotImplementedError("FASE ROJA: Implementar validación de header")


def validate_not_encrypted(content: bytes) -> Any:
    """Valida que el PDF no esté cifrado con contraseña.

    Retorna el documento fitz abierto si es válido.
    """
    raise NotImplementedError("FASE ROJA: Implementar validación de cifrado")


def validate_has_pages(doc: Any) -> bool:
    """Valida que el PDF tenga al menos 1 página."""
    raise NotImplementedError("FASE ROJA: Implementar validación de páginas")


def validate_has_text(doc: Any) -> bool:
    """Valida que el PDF tenga texto extraíble.

    Umbral: más de 10 caracteres en total.
    """
    raise NotImplementedError("FASE ROJA: Implementar validación de texto")


def validate_pdf_complete(file: Any, content: bytes) -> bool:
    """Validación completa: ejecuta todas las validaciones en orden.

    Orden de validaciones:
    1. Existencia
    2. Tamaño
    3. Extensión
    4. Header
    5. Cifrado (retorna doc fitz)
    6. Páginas
    7. Texto
    """
    raise NotImplementedError("FASE ROJA: Implementar validación completa")
