import boto3
from botocore.exceptions import BotoCoreError, ClientError
from app.core.config import config
from contextlib import contextmanager

from app.core.logger import log_error


class DynamoDBConnection:
    """
    Configura y gestiona la conexión a DynamoDB utilizando credenciales de AWS.
    """

    def __init__(self, region_name: str = config.AWS_REGION):
        self._dynamodb = None
        self.region_name = region_name  # Región donde se encuentra la tabla

    @property
    def dynamodb(self):
        """
        Obtiene una instancia de DynamoDB, inicializándola si no existe.
        """
        if not self._dynamodb:
            # No se pasan credenciales explícitas
            self._dynamodb = boto3.resource('dynamodb', region_name=self.region_name)
        return self._dynamodb

    def get_table(self, table_name: str):
        """
        Obtiene una referencia a una tabla específica en DynamoDB.
        """
        try:
            return self.dynamodb.Table(table_name)
        except (BotoCoreError, ClientError) as e:
            raise Exception(f"Error al obtener la tabla {table_name}: {e}")


@contextmanager
def dynamo_table(table_name: str):
    """
    Context manager para manejar operaciones con una tabla DynamoDB.
    """
    connection = DynamoDBConnection()
    table = connection.get_table(table_name)
    try:
        yield table
    except Exception as e:
        log_error(f"Error durante la operación con la tabla {table_name}: {e}")
        raise

