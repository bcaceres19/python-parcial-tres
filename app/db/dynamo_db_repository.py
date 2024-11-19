from app.core.dynamo_db_connection import dynamo_table
from botocore.exceptions import ClientError
from typing import Dict, Any


class DynamoDbRepository:
    """
    Repositorio para interactuar con la tabla DynamoDB "Estudiantes".
    """

    def __init__(self, table_name: str = "Estudiantes"):
        self.table_name = table_name

    def insert_item(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """
        Inserta un ítem en la tabla de DynamoDB.

        Args:
            item (Dict[str, Any]): Diccionario con los datos del ítem a insertar.

        Returns:
            Dict[str, Any]: El ítem insertado o una excepción en caso de error.

        Raises:
            ClientError: Si ocurre un error específico de AWS.
            Exception: Si ocurre un error inesperado.
        """
        with dynamo_table(self.table_name) as table:
            try:
                table.put_item(Item=item)
                return {"message": "Item insertado correctamente", "item": item}
            except ClientError as e:
                # Levantar el error capturado con detalles del mensaje
                raise Exception(
                    f"Error al insertar el ítem en la tabla '{self.table_name}': {e.response['Error']['Message']}"
                ) from e
            except Exception as e:
                # Manejar errores inesperados
                raise Exception(f"Error inesperado al insertar el ítem: {str(e)}") from e

    def get_item_by_id(self, item_id: str) -> Dict[str, Any]:
        """
        Obtiene un ítem de DynamoDB por su ID.

        Args:
            item_id (str): ID del ítem a buscar.

        Returns:
            Dict[str, Any]: El ítem encontrado o un mensaje si no existe.

        Raises:
            ClientError: Si ocurre un error específico de AWS.
            Exception: Si ocurre un error inesperado.
        """
        with dynamo_table(self.table_name) as table:
            try:
                response = table.get_item(Key={"id": item_id})
                if "Item" in response:
                    return {"message": "Item encontrado", "item": response["Item"]}
                return {"message": f"Item con ID '{item_id}' no encontrado."}
            except ClientError as e:
                raise Exception(
                    f"Error al obtener el ítem de la tabla '{self.table_name}': {e.response['Error']['Message']}"
                ) from e
            except Exception as e:
                raise Exception(f"Error inesperado al obtener el ítem: {str(e)}") from e
