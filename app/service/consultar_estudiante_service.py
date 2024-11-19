from fastapi import HTTPException
from app.core.dynamo_db_connection import DynamoDBConnection
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
        """
        Consulta un estudiante por ID en la tabla DynamoDB.

        Args:
            id_item (str): ID del estudiante a buscar.

        Returns:
            ResponseGeneral: Objeto con el estado de la operación y los datos.
        """
        try:
            # Buscar el ítem en DynamoDB
            item = self.repository.get_item_by_id(id_item)

            if "error" in item:
                # Si ocurre un error en el repositorio, devolvemos un error
                log_error(item)
                return HTTPException(
                    detail=f"Error al consultar el estudiante: {item['error']}",
                    status_code=500
                )
            if "message" in item:
                # Si no se encuentra el ítem
                log_error(item)
                return HTTPException(
                    detail=item["message"],
                    status_code=404,
                )

            # Respuesta de éxito
            return ResponseGeneral(
                mensaje="Estudiante consultado correctamente.",
                status=200,
                data=item
            )
        except ClientError as e:
            # Manejo específico de errores de DynamoDB
            log_error(e)
            return HTTPException(
                detail=f"Error al consultar el estudiante: {e.response['Error']['Message']}",
                status_code=500
            )
        except Exception as e:
            # Manejo de errores generales
            log_error(e)
            return HTTPException(
                detail=f"Error inesperado: {str(e)}",
                status_code=500
            )
