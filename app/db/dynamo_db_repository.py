from app.core.dynamo_db_connection import dynamo_table
from botocore.exceptions import ClientError

from app.core.logger import log_error


class DynamoDbRepository:
    """
    Repositorio para interactuar con la tabla DynamoDB "Estudiantes".
    """

    def __init__(self, table_name: str = "Estudiantes"):
        self.table_name = table_name
        
    def insert_item(self, item: dict):
        """
        Inserta un ítem en la tabla de DynamoDB.

        Args:
            item (dict): Diccionario con los datos del ítem a insertar.

        Returns:
            dict: Mensaje de éxito o error.
        """
        with dynamo_table(self.table_name) as table:
            try:
                log_error("Encontro la tabla")
                # Insertar el ítem en la tabla
                table.put_item(Item=item)
                return item
            except ClientError as e:
                log_error(e)
                return {"error": f"Error al insertar el ítem: {e.response['Error']['Message']}"}
            except Exception as e:
                log_error(e)
                return {"error": f"Error inesperado al insertar el ítem: {str(e)}"}

    def get_item_by_id(self, item_id: str):
        """
        Obtiene un ítem de DynamoDB por su ID.

        Args:
            item_id (str): ID del ítem a buscar.

        Returns:
            dict: El ítem encontrado o un mensaje de error.
        """
        with dynamo_table(self.table_name) as table:
            try:
                response = table.get_item(Key={'id': item_id})
                if 'Item' in response:
                    return response['Item']
                return {"message": f"Item con ID {item_id} no encontrado."}
            except ClientError as e:
                log_error(e)
                return {"error": f"Error al obtener el ítem: {e.response['Error']['Message']}"}
            except Exception as e:
                log_error(e)
                return {"error": f"Error inesperado al obtener el ítem: {str(e)}"}