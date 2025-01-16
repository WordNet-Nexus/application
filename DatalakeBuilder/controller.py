from src.clean.cleaner import TextCleaner
from src.hazelcast_client import HazelcastClientManager
from src.uploader.uploaders import Uploaders
from config.settings import TEMP_FOLDER, TABLE_NAME, BUCKET_NAME, MONGO_HOST, MONGO_PORT, START_ID, END_ID
from src.bookFetcher.book_fetcher import BookFetcher

class Controller:

    @staticmethod
    def initialize():
        print("Initializing Controller")
        downloader = BookFetcher.initialize_downloader("AWS")
        print("Connected to AWS")
        cleaner = TextCleaner()
        print("Text Cleaner initialized")
        hazelcast_manager = HazelcastClientManager()
        print("Connected to Hazelcast")
        Controller.downloader_controller(downloader, cleaner, hazelcast_manager)
        Controller.uploader_controller(hazelcast_manager)
        hazelcast_manager.shutdown()
        
    @staticmethod
    def downloader_controller(downloader, cleaner, hazelcast_manager):
        for file_path in downloader.download(BUCKET_NAME, TEMP_FOLDER, START_ID, END_ID):
            print(f"Processing file: {file_path}")
            word_counts = cleaner.process_documents(file_path)
            hazelcast_manager.update_word_map(word_counts)
            downloader.delete_temp_file(file_path)
    
    @staticmethod
    def uploader_controller(hazelcast_manager):
        uploader = Uploaders.initialize_uploader('MongoDBAWS', TABLE_NAME)
        uploader.set_params(MONGO_HOST, MONGO_PORT)
        uploader.create_collection()
        data_to_upload = hazelcast_manager.get_word_map_data()
        uploader.upload_data(data_to_upload)