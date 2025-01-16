import unittest
from unittest.mock import patch, MagicMock
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../IsolatedNodes/lambda_package')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../IsolatedNodes/webpage')))

os.environ["NEO4J_URI"] = "bolt://localhost:7687"
os.environ["NEO4J_USER"] = "neo4j"
os.environ["NEO4J_PASSWORD"] = "password"

try:
    from lambda_function import lambda_handler, query_isolated_nodes
    from query_handler import QueryHandler
except ImportError:
    lambda_handler = None
    query_isolated_nodes = None
    QueryHandler = None


class TestIsolatedNodes(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.mock_lambda_client = patch("boto3.client").start()
        cls.mock_lambda_client.return_value.invoke = MagicMock(
            return_value={
                "Payload": MagicMock(
                    read=MagicMock(
                        return_value=b'{"body": "[\\"node1\\", \\"node2\\"]"}'
                    )
                )
            }
        )

        cls.mock_driver = patch("lambda_function.GraphDatabase.driver").start()

    @classmethod
    def tearDownClass(cls):
        patch.stopall()

    def test_lambda_handler_valid(self):
        """Invalid lambda_handler."""
        if lambda_handler:
            mock_driver_instance = self.mock_driver.return_value
            mock_session = mock_driver_instance.session.return_value.__enter__.return_value
            mock_session.run.return_value = [{"nodeId": "node1"}, {"nodeId": "node2"}]

            mock_event = {}
            context = MagicMock()
            response = lambda_handler(mock_event, context)
            self.assertEqual(response["statusCode"], 200)
            self.assertIn("node1", response["body"])
        else:
            self.fail("lambda_handler could not be imported.")

    def test_query_isolated_nodes(self):
        """valid query_isolated_nodes."""
        if query_isolated_nodes:
            mock_driver_instance = self.mock_driver.return_value
            mock_session = mock_driver_instance.session.return_value.__enter__.return_value
            mock_session.run.return_value = [{"nodeId": "node1"}, {"nodeId": "node2"}]

            result = query_isolated_nodes(mock_driver_instance)
            self.assertEqual(len(result), 2)
            self.assertIn("node1", result)
            self.assertIn("node2", result)
        else:
            self.fail("query_isolated_nodes could not be imported.")

    @patch("query_handler.boto3.client")
    def test_query_handler_invoke_lambda(self, mock_boto_client):
        """Invalid invoke_lambda in QueryHandler."""
        if QueryHandler:
            mock_lambda_client = MagicMock()
            mock_lambda_client.invoke.return_value = {
                "Payload": MagicMock(
                    read=MagicMock(
                        return_value=b'{"body": "[\\"node1\\", \\"node2\\"]"}'
                    )
                )
            }
            mock_boto_client.return_value = mock_lambda_client

            handler = QueryHandler()
            response = handler.invoke_lambda()
            self.assertIsInstance(response, list)
            self.assertIn("node1", response)
        else:
            self.fail("QueryHandler could not be imported.")

    def test_query_handler_exception(self):
        """Exceptions for invoke_lambda."""
        if QueryHandler:
            handler = QueryHandler()
            handler.lambda_client.invoke.side_effect = Exception("Error in Lambda")
            with self.assertRaises(Exception):
                handler.invoke_lambda()
        else:
            self.fail("QueryHandler could not be imported.")


if __name__ == "__main__":
    unittest.main()
