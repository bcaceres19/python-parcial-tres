from fastapi import HTTPException
from app.core.dynamo_db_connection import DynamoDBConnection, config
from app.db.dynamo_db_repository import DynamoDbRepository
from app.schemas.response_general import ResponseGeneral
from botocore.exceptions import ClientError
from app.core.logger import log_error

class ConsultarEstudianteService:
    """
    Servicio para consultar estudiantes en DynamoDB.
    """

    def __init__(self):
        # Inicializa el repositorio para interactuar con DynamoDB
        self.repository = DynamoDbRepository()

    def consultar_estudiante_id(self, id_item: str) -> ResponseGeneral:
        try:
            item = self.repository.get_item_by_id(id_item)
            if "error" in item:
                log_error(item)
                return ResponseGeneral(
                    mensaje=f"Error al consultar el estudiante: {item['error']}",
                    status=500,
                    data=None
                )
            if "message" in item:
                return ResponseGeneral(
                    mensaje=item["message"],
                    status=404,
                    data=None
                )
            return ResponseGeneral(
                mensaje="Estudiante consultado correctamente.",
                status=200,
                data=item
            )
        except ClientError as e:
            log_error(e)
            return ResponseGeneral(
                mensaje=f"Error al consultar el estudiante: {e.response['Error']['Message']}",
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
