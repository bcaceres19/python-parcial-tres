import uuid

from fastapi import HTTPException
from app.db.dynamo_db_repository import DynamoDbRepository
from app.schemas.estudiantes import Estudiantes
from app.schemas.response_general import ResponseGeneral
from botocore.exceptions import ClientError
from app.core.logger import log_error


class GuardarEstudianteService:
    """
    Servicio para guardar un estudiante en DynamoDB.
    """

    def __init__(self):
        # Usa el repositorio para interactuar con DynamoDB
        self.repository = DynamoDbRepository()

    def guardar_estudiante(self, estudiante: Estudiantes) -> ResponseGeneral:    
        """
        Guarda un estudiante en la tabla DynamoDB.

        Args:
            estudiante (Estudiantes): Objeto con los datos del estudiante.

        Returns:
            ResponseGeneral: Objeto de respuesta con el estado de la operación.
        """
        try:
            # Generar un ID único para el estudiante
            estudiante.id = str(uuid.uuid4())  # Corregido: Se usa uuid.uuid4()
            
            # Insertar el estudiante usando el repositorio
            resultado = self.repository.insert_item(estudiante.model_dump())  # Usar model_dump() en lugar de dict() si es Pydantic v2
            if "error" in resultado:
                # Si ocurre un error en el repositorio, devolvemos un error
                log_error(resultado)
                return HTTPException(
                    detail=f"Error al crear el estudiante: {resultado['error']}",
                    status_code=500
                )
            # Crear respuesta de éxito
            return ResponseGeneral(
                mensaje="Estudiante guardado correctamente.",
                status=201,
                data=resultado
            )
        except ClientError as e:
            # Manejo específico de errores de DynamoDB
            log_error(e)
            return HTTPException(
                detail=f"Error al guardar el estudiante: {e.response['Error']['Message']}",
                status_code=500
            )
        except Exception as e:
            # Manejo general de errores
            log_error(e)
            return HTTPException(
                detail=f"Error inesperado: {str(e)}",
                status_code=500
            )
