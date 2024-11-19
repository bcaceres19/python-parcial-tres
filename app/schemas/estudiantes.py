from typing import Optional
from pydantic import BaseModel, Field


class Estudiantes(BaseModel):
    """
    Modelo para representar un estudiante.
    """
    id: Optional[str] = Field(
        default=None,
        description="ID único del estudiante, generado automáticamente si no se proporciona."
    )
    nombre: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Nombre completo del estudiante. Debe tener entre 2 y 100 caracteres."
    )
    carrera: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Carrera del estudiante. Debe tener entre 2 y 100 caracteres."
    )
