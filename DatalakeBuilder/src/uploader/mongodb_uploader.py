from pymongo import MongoClient
from pymongo.errors import PyMongoError

class MongoDBUploader:
    def __init__(self, database_name):
        self.client = None
        self.database_name = database_name
        self.collection_name = database_name
        self.db = None
        self.collection = None
    
    def set_params(self, host, port):
        mongo_uri = f"mongodb://{host}:{port}/"
        self.client = MongoClient(mongo_uri)
        self.collection_name = self.database_name
        self.db = self.client[self.database_name]
        self.collection = self.db[self.collection_name]

    def upload_data(self, data):
        try:
            documents = [{"word": word, "count": count} for word, count in data.items()]
            self.collection.insert_many(documents)
        except PyMongoError as e:
            print(f"Error al subir datos a MongoDB: {e}")

    def create_collection(self):
        try:
            if self.collection_name in self.db.list_collection_names():
                return

            self.db.create_collection(self.collection_name)
        except PyMongoError as e:
            print(f"Error al crear la colección en MongoDB: {e}")
