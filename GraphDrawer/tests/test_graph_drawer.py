import unittest
from unittest.mock import patch, MagicMock
from pymongo import MongoClient
import hazelcast
import config.settings as config
from src.download_words.aws_words_downloaders import AWSWordsDownloader
from src.download_words.downloaders import Downloaders
from src.graph_builder.word_checker import WordChecker
from src.storage.aws_storage_neo4j import AWSStorageNeo4J
from src.storage.aws_storage_neptune import AWSStorageNeptune
from src.storage.graph_store import GraphStore

class TestGraphDrawer(unittest.TestCase):

    def setUp(self):
        """Set up shared resources for tests."""
        self.mock_mongo_client = MagicMock()
        self.mock_hazelcast_client = MagicMock()
        self.mock_neo4j_driver = MagicMock()
        self.mock_boto3_client = MagicMock()

    @patch('pymongo.MongoClient')
    @patch('hazelcast.HazelcastClient')
    def test_aws_words_downloader_run(self, mock_hazelcast_client, mock_mongo_client):
        """Test the run method of AWSWordsDownloader."""
        mock_mongo_client.return_value = self.mock_mongo_client
        mock_hazelcast_client.return_value = self.mock_hazelcast_client

        downloader = AWSWordsDownloader()
        downloader.connect_mongo = MagicMock()
        downloader.connect_hazelcast = MagicMock()
        downloader.download_from_mongo = MagicMock(return_value={"word1": 5, "word2": 3})
        downloader.upload_to_hazelcast = MagicMock()
        downloader.close_connections = MagicMock()

        downloader.run()

        downloader.connect_mongo.assert_called_once()
        downloader.connect_hazelcast.assert_called_once()
        downloader.download_from_mongo.assert_called_once()
        downloader.upload_to_hazelcast.assert_called_once_with({"word1": 5, "word2": 3})
        downloader.close_connections.assert_called_once()

    def test_word_checker_are_one_letter_apart(self):
        """Test WordChecker.are_one_letter_apart."""
        self.assertTrue(WordChecker.are_one_letter_apart("cat", "bat"))
        self.assertFalse(WordChecker.are_one_letter_apart("cat", "dog"))
        self.assertTrue(WordChecker.are_one_letter_apart("cat", "cats"))
        self.assertTrue(WordChecker.are_one_letter_apart("cat", "at"))

    @patch('neo4j.GraphDatabase.driver')
    def test_aws_storage_neo4j_upload_edges(self, mock_graphdb_driver):
        """Test uploading edges to Neo4j."""
        mock_graphdb_driver.return_value = self.mock_neo4j_driver

        storage = AWSStorageNeo4J("bolt://localhost:7687", "user", "password")
        storage.driver = self.mock_neo4j_driver

        edges = [("word1", "word2", 0.5, 5, 3)]
        storage.upload_edges(edges)

        self.mock_neo4j_driver.session.assert_called_once()

    @patch('boto3.client')
    def test_aws_storage_neptune_load_graph(self, mock_boto3_client):
        """Test loading graph into AWS Neptune."""
        mock_boto3_client.return_value = self.mock_boto3_client

        storage = AWSStorageNeptune(graph=MagicMock())
        storage.graph.nodes = MagicMock(return_value=[("word1", {"frequency": 5})])
        storage.graph.edges = MagicMock(return_value=[("word1", "word2", {"weight": 0.5})])

        storage.load_graph()

        self.mock_boto3_client.execute_gremlin_query.assert_called()

    def test_graph_store_abstract_load_graph(self):
        """Test GraphStore abstract load_graph method."""
        with self.assertRaises(TypeError):
            GraphStore()

if __name__ == '__main__':
    unittest.main()
