import os

TEMP_FOLDER = os.getenv('TEMP_FOLDER', os.path.join(os.getcwd(), "DatalakeBuilder/data", "documents"))
TABLE_NAME = os.getenv('TABLE_NAME', "WordCounts")
HAZELCAST_CLUSTER_MEMBERS = os.getenv('HAZELCAST_CLUSTER_MEMBERS', "127.0.0.1:5701").split(',')
REGION_NAME = os.getenv('REGION_NAME', "us-east-1")
BUCKET_NAME = os.getenv('BUCKET_NAME', "wordnetnexus-gutenberg-ulpgc")
MONGO_HOST = os.getenv('MONGO_HOST', "54.172.88.36")
MONGO_PORT = int(os.getenv('MONGO_PORT', 27017))
START_ID = int(os.getenv('START_ID', 1))
END_ID = int(os.getenv('END_ID', 10))
