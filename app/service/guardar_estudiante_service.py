import uuid

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
        try:
            estudiante.id = str(uuid.uuid4())  # Generar un ID único
            resultado = self.repository.insert_item(estudiante.model_dump())
            if "error" in resultado:
                log_error(resultado)
                return ResponseGeneral(
                    mensaje=f"Error al crear el estudiante: {resultado['error']}",
                    status=500,
                    data=None
                )
            return ResponseGeneral(
                mensaje="Estudiante guardado correctamente.",
                status=201,
                data=resultado
            )
        except ClientError as e:
            log_error(e)
            return ResponseGeneral(
                mensaje=f"Error al guardar el estudiante: {e.response['Error']['Message']}",
                status=500,
                data=None
            )
        except Exception as e:
            log_error(e)
            return ResponseGeneral(
                mensaje=f"Error inesperado: {str(e)}",
                status=500,
                data=None
            )

