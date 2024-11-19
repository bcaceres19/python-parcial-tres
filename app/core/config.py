"""
Este módulo contiene la configuración de la aplicación, utilizando Pydantic para manejar las
variables de entorno.
"""

from pydantic_settings import BaseSettings
from pydantic import Field, field_validator
from dotenv import load_dotenv
import os

load_dotenv()


class Config(BaseSettings):
    """
    Clase de configuración utilizando Pydantic para manejar variables de entorno.
    """
    APP_NAME: str = Field("My FastAPI App", env="APP_NAME")
    DEBUG: bool = Field(False, env="DEBUG")

    # Configuración de base de datos
    MAX_CONNECTIONS_COUNT: int = Field(10, env="MAX_CONNECTIONS_COUNT")
    MIN_CONNECTIONS_COUNT: int = Field(10, env="MIN_CONNECTIONS_COUNT")

    RUTA_BASE: str = Field("/api", env="RUTA_BASE")

    # Configuración de AWS
    AWS_ACCESS_KEY_ID: str = Field(..., env="AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY: str = Field(..., env="AWS_SECRET_ACCESS_KEY")
    AWS_REGION: str = Field("us-east-1", env="AWS_REGION")


    # Validación para convertir el valor de DEBUG correctamente
    @field_validator("DEBUG", mode="before")
    @classmethod
    def parse_debug(cls, value):
        """
        Valida y convierte el valor de DEBUG.

        Args:
            value: El valor de la variable DEBUG.

        Returns:
            bool: El valor convertido en booleano.
        """
        if isinstance(value, str):
            return value.lower() in ("true", "1")
        return value

    class Config:  # pylint: disable=too-few-public-methods
        """
        Clase de configuración interna para definir el archivo de entorno a usar.
        """
        env_file = ".env"  # Define el archivo de entorno a usar


# Instanciar la configuración
config = Config()
