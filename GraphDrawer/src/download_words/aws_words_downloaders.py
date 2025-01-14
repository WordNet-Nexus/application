from pymongo import MongoClient
import hazelcast
import config.settings as config


class AWSWordsDownloader:

    def __init__(self):
        self.mongo_host = config.MONGO_HOST
        self.mongo_port = config.MONGO_PORT
        self.mongo_db_name = config.MONGO_DB_NAME
        self.collection_name = config.COLLECTION_NAME

        self.hazelcast_cluster_members = config.HAZELCAST_CLUSTER_MEMBERS
        self.hazelcast_cluster_name = config.CLUSTER_NAME
        self.dict_name = config.DICT_NAME

        self.mongo_client = None
        self.mongo_collection = None
        self.hazelcast_client = None
        self.words_map = None
        print("AWSWordsDownloader initialized.")
        print(f"MongoDB: {self.mongo_host}:{self.mongo_port}/{self.mongo_db_name}/{self.collection_name}")

    def connect_mongo(self):
        uri = f"mongodb://{self.mongo_host}:{self.mongo_port}/"
        self.mongo_client = MongoClient(uri)
        db = self.mongo_client[self.mongo_db_name]
        self.mongo_collection = db[self.collection_name]

    def connect_hazelcast(self):
        self.hazelcast_client = hazelcast.HazelcastClient(
            cluster_members=self.hazelcast_cluster_members,
            cluster_name=self.hazelcast_cluster_name
        )
        self.words_map = self.hazelcast_client.get_map(self.dict_name).blocking()

    def download_from_mongo(self):
        word_counts = {}
        for doc in self.mongo_collection.find():
            word = doc["word"]
            count = doc["count"]
            word_counts[word] = count
        return word_counts

    def upload_to_hazelcast(self, word_counts):
        for word, count in word_counts.items():
            self.words_map.put(word, count)

    def close_connections(self):
        if self.hazelcast_client is not None:
            self.hazelcast_client.shutdown()
        if self.mongo_client is not None:
            self.mongo_client.close()

    def run(self):
        self.connect_mongo()
        self.connect_hazelcast()
        data = self.download_from_mongo()
        self.upload_to_hazelcast(data)
        self.close_connections()
