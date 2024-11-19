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
        self.region_name = region_name
        self.aws_access_key_id = config.AWS_ACCESS_KEY_ID
        self.aws_secret_access_key = config.AWS_SECRET_ACCESS_KEY

    @property
    def dynamodb(self):
        """
        Obtiene una instancia de DynamoDB, inicializándola si no existe.
        """
        if not self._dynamodb:
            self._dynamodb = boto3.resource(
                'dynamodb',
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
                region_name=self.region_name
            )
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
    log_error("Encontro la tabla")
    try:
        yield table
    except Exception as e:
        raise Exception(f"Error durante la operación con la tabla {table_name}: {e}")
