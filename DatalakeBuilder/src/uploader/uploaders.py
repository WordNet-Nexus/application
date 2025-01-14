from src.uploader.dynamodb_uploader import DynamoDBUploader
from src.uploader.mongodb_uploader import MongoDBUploader
class Uploaders:

    __uploaders_keys = {
        'dynamodbAWS': DynamoDBUploader,
        'MongoDBAWS': MongoDBUploader
    }

    @staticmethod
    def initialize_uploader(uploader_key, table_name):
        return Uploaders.__uploaders_keys[uploader_key](table_name)