import unittest
from DatalakeBuilder.src.clean.cleaner import TextCleaner
from DatalakeBuilder.src.bookFetcher.book_fetcher import BookFetcher
from DatalakeBuilder.src.uploader.mongodb_uploader import MongoDBUploader
from unittest.mock import patch, MagicMock
from collections import Counter

class TestTextCleaner(unittest.TestCase):
    def setUp(self):
        self.cleaner = TextCleaner()

    @patch("DatalakeBuilder.src.clean.cleaner.stopwords.words", return_value=["the", "and", "is", "in", "this", "an", "with"])
    def test_clean_text(self, mock_stopwords):
        text = "This is an example text, with numbers 123 and punctuation!"
        cleaned_text = self.cleaner.clean_text(text)
        self.assertEqual(cleaned_text, ["example", "text", "numbers", "punctuation"])

    def test_process_documents(self):
        with patch("builtins.open", unittest.mock.mock_open(read_data="This is a test file.")):
            with patch("os.path.isfile", return_value=True):
                result = self.cleaner.process_documents("fake_path.txt")
                self.assertIsInstance(result, Counter)
                self.assertGreater(len(result), 0)


class TestBookFetcher(unittest.TestCase):
    def test_initialize_downloader(self):
        fetcher = BookFetcher.initialize_downloader("AWS")
        self.assertIsNotNone(fetcher)

class TestMongoDBUploader(unittest.TestCase):
    @patch("DatalakeBuilder.src.uploader.mongodb_uploader.MongoClient")
    def test_set_params(self, mock_mongo_client):
        uploader = MongoDBUploader(database_name="test_db")
        uploader.set_params(host="localhost", port=27017)
        self.assertIsNotNone(uploader.client)

    @patch("DatalakeBuilder.src.uploader.mongodb_uploader.MongoClient")
    def test_upload_data(self, mock_mongo_client):
        mock_db = MagicMock()
        mock_collection = MagicMock()
        mock_mongo_client.return_value.__getitem__.return_value = mock_db
        mock_db.__getitem__.return_value = mock_collection
        uploader = MongoDBUploader(database_name="test_db")
        uploader.set_params(host="localhost", port=27017)

        sample_data = {"word1": 5, "word2": 10}
        uploader.upload_data(sample_data)
        expected_calls = [
            (({"word": "word1"}, {"$set": {"word": "word1", "count": 5}}), {"upsert": True}),
            (({"word": "word2"}, {"$set": {"word": "word2", "count": 10}}), {"upsert": True}),
        ]
        mock_collection.update_one.assert_has_calls(expected_calls, any_order=True)

    @patch("DatalakeBuilder.src.uploader.mongodb_uploader.MongoClient")
    def test_create_collection(self, mock_mongo_client):
        mock_db = MagicMock()
        mock_mongo_client.return_value.__getitem__.return_value = mock_db

        uploader = MongoDBUploader(database_name="test_db")
        uploader.client = mock_mongo_client
        uploader.db = mock_db

        mock_db.list_collection_names.return_value = []
        uploader.create_collection()
        mock_db.create_collection.assert_called_once_with("test_db")

if __name__ == '__main__':
    unittest.main()