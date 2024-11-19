from pydantic import BaseModel, Field


class TextInput(BaseModel):
    """
    Esquema Pydantic para representar entradas de texto.

    Incluye validaciones de longitud mínima y máxima y documentación para una mejor comprensión.
    """
    texto: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="Texto de entrada para ser procesado. Debe tener entre 1 y 1000 caracteres."
    )
