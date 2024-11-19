from pydantic import BaseModel, Field, PositiveInt


class TextResponse(BaseModel):
    """
    Esquema Pydantic para representar la respuesta al procesamiento de texto.

    Incluye información sobre el número de palabras, el número de caracteres,
    y el texto transformado a mayúsculas.
    """
    numero_palabras: PositiveInt = Field(
        ...,
        description="Cantidad de palabras en el texto procesado. Debe ser un número entero positivo."
    )
    numero_caracteres: PositiveInt = Field(
        ...,
        description="Cantidad de caracteres en el texto procesado. Debe ser un número entero positivo."
    )
    texto_mayusculas: str = Field(
        ...,
        description="Texto original transformado a mayúsculas."
    )
