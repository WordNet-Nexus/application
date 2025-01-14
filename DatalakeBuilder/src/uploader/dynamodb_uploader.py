import boto3
from botocore.exceptions import BotoCoreError, ClientError
from config.settings import REGION_NAME

class DynamoDBUploader:
    def __init__(self, table_name):
        self.session = boto3.Session()
        self.dynamodb = self.session.resource("dynamodb", region_name=REGION_NAME)
        self.table_name = table_name
        self.table = self.dynamodb.Table(self.table_name)

    def upload_data(self, data):
        try:
            with self.table.batch_writer() as batch:
                for word, count in data.items():
                    batch.put_item(Item={"word": word, "count": count})
            print("Datos subidos a DynamoDB exitosamente.")
        except (BotoCoreError, ClientError) as e:
            print(f"Error al subir datos a DynamoDB: {e}")
    
    def create_table(self):
        try:
            dynamodb_client = self.session.client("dynamodb", region_name=REGION_NAME)
            existing_tables = dynamodb_client.list_tables()["TableNames"]
            if self.table_name in existing_tables:
                return

            response = dynamodb_client.create_table(
                TableName=self.table_name,
                KeySchema=[
                    {"AttributeName": "word", "KeyType": "HASH"}
                ],
                AttributeDefinitions=[
                    {"AttributeName": "word", "AttributeType": "S"}
                ],
                ProvisionedThroughput={
                    "ReadCapacityUnits": 5,
                    "WriteCapacityUnits": 5
                }
            )

        except (BotoCoreError, ClientError) as e:
            raise e