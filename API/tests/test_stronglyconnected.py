import os
import unittest
from unittest.mock import patch, MagicMock, PropertyMock

os.environ["NEO4J_URI"] = "bolt://mocked:7687"
os.environ["NEO4J_USER"] = "mock_user"
os.environ["NEO4J_PASSWORD"] = "mock_password"

with patch("StronglyConnected.query_handler.GraphDatabase.driver", new_callable=MagicMock):
    from StronglyConnected.query_handler import QueryHandler
    from StronglyConnected.app import app


class TestAppRoutes(unittest.TestCase):
    
    def setUp(self):
        """Set up the Flask test client."""
        self.app = app.test_client()
        self.app.testing = True

    def test_index_route(self):
        """Test the index route."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_display_route_missing_params(self):
        """Test the display route with missing parameters."""
        with app.test_request_context('/display', method='GET'):
            with patch("StronglyConnected.app.request.args", return_value={}):
                response = self.app.get('/display')
                self.assertEqual(response.status_code, 200)

    def test_display_route_invalid_algorithm(self):
        """Test the display route with an invalid algorithm."""
        with app.test_request_context('/display', method='GET'):
            with patch("StronglyConnected.app.request.args", return_value={"algorithm": "invalid", "cluster": "1"}):
                response = self.app.get('/display?algorithm=invalid&cluster=1')
                self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
