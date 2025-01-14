import unittest
from unittest.mock import patch, MagicMock
import os
import json
from MaxDistance.lambda_package.lambda_function import find_longest_path_by_steps, find_longest_path_by_weight
from MaxDistance.webpage.query_handler import QueryHandler

# Mock de variables de entorno
os.environ["NEO4J_URI"] = "bolt://localhost:7687"
os.environ["NEO4J_USER"] = "neo4j"
os.environ["NEO4J_PASSWORD"] = "password"


class TestMaxDistance(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Mock del cliente Lambda de AWS
        cls.mock_lambda_client = patch("boto3.client").start()
        cls.mock_lambda_client.return_value.invoke = MagicMock(
            return_value={
                "Payload": MagicMock(
                    read=MagicMock(
                        return_value=json.dumps({
                            "statusCode": 200,
                            "body": json.dumps([{"nodes": ["word1", "word2"], "length": 2}])
                        })
                    )
                )
            }
        )

    @classmethod
    def tearDownClass(cls):
        patch.stopall()

    def test_lambda_handler_missing_params(self):
        """Prueba para parámetros faltantes en lambda_handler."""
        mock_event = {
            "start_word": "word1"
        }
        context = MagicMock()
        from MaxDistance.lambda_package.lambda_function import lambda_handler
        response = lambda_handler(mock_event, context)
        self.assertEqual(response["statusCode"], 400)
        body = json.loads(response["body"])
        self.assertIn("start_word and end_word are required", body["error"])

    def test_lambda_handler_invalid_mode(self):
        """Prueba para modo inválido en lambda_handler."""
        mock_event = {
            "start_word": "word1",
            "end_word": "word2",
            "mode": "invalid_mode"
        }
        context = MagicMock()
        from MaxDistance.lambda_package.lambda_function import lambda_handler
        response = lambda_handler(mock_event, context)
        self.assertEqual(response["statusCode"], 400)
        body = json.loads(response["body"])
        self.assertIn("Invalid mode", body["error"])

    @patch("MaxDistance.webpage.query_handler.QueryHandler.invoke_lambda")
    def test_query_handler_invoke_lambda(self, mock_invoke_lambda):
        """Prueba válida para invoke_lambda en QueryHandler."""
        mock_invoke_lambda.return_value = [{"nodes": ["word1", "word2"], "length": 2}]
        handler = QueryHandler()
        response = handler.invoke_lambda("word1", "word2", "steps", 10)
        self.assertEqual(response[0]["nodes"], ["word1", "word2"])
        self.assertEqual(response[0]["length"], 2)

    def test_find_longest_path_by_steps(self):
        """Prueba para find_longest_path_by_steps."""
        mock_tx = MagicMock()
        mock_tx.run.return_value = iter([
            {
                "p": MagicMock(
                    nodes=[{"id": "word1"}, {"id": "word2"}],
                    relationships=[{"weight": 1}]
                ),
                "pathLength": 2
            }
        ])
        result = find_longest_path_by_steps(mock_tx, "word1", "word2", 10)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["nodes"], ["word1", "word2"])
        self.assertEqual(result[0]["length"], 2)

    def test_find_longest_path_by_weight(self):
        """Prueba para find_longest_path_by_weight."""
        mock_tx = MagicMock()
        mock_tx.run.return_value = iter([
            {
                "p": MagicMock(
                    nodes=[{"id": "word1"}, {"id": "word2"}],
                    relationships=[{"weight": 5}]
                ),
                "totalWeight": 5
            }
        ])
        result = find_longest_path_by_weight(mock_tx, "word1", "word2", 10)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["nodes"], ["word1", "word2"])
        self.assertEqual(result[0]["total_weight"], 5)


if __name__ == "__main__":
    unittest.main()
