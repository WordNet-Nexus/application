import os

HAZELCAST_CLUSTER_MEMBERS = os.getenv("HAZELCAST_CLUSTER_MEMBERS", "127.0.0.1:5702").split(",")
CLUSTER_NAME = os.getenv("CLUSTER_NAME", "myGraph")
DICT_NAME = os.getenv("DICT_NAME", "word_frequencies")
MONGO_HOST = os.getenv("MONGO_HOST", "127.0.0.1")
MONGO_PORT = int(os.getenv("MONGO_PORT", 27017))
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "WordCounts")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "WordCounts")
URI = os.getenv("URI", "bolt://localhost:7687")
USER = os.getenv("USER", "neo4j")
PASSWORD = os.getenv("NEO4J_PASSWORD", "password")