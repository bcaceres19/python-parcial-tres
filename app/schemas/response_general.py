from typing import Any, Dict, Optional, Union, List
from pydantic import BaseModel, Field, PositiveInt


class ResponseGeneral(BaseModel):
    """
    Esquema Pydantic para representar una respuesta general estándar.

    Este modelo incluye:
    - Un mensaje descriptivo.
    - Un código de estado HTTP positivo.
    - Datos opcionales que pueden ser de cualquier tipo, como un diccionario o una lista.
    """
    mensaje: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Mensaje descriptivo de la respuesta."
    )
    status: PositiveInt = Field(
        ...,
        ge=100,
        le=599,
        description="Código de estado HTTP. Debe estar entre 100 y 599."
    )
    data: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = Field(
        default=None,
        description=(
            "Datos adicionales relacionados con la respuesta. Puede ser un diccionario o una lista de diccionarios."
        )
    )
