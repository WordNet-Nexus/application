import unittest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

with patch('NodeConnections.query_handler.QueryHandler', autospec=True) as MockQueryHandler:
    mock_instance = MockQueryHandler.return_value

    mock_instance.get_nodes_by_degree.return_value = [
        {"id": "node1", "frequency": 10, "relationships": 2},
        {"id": "node2", "frequency": 5, "relationships": 2},
    ]
    mock_instance.get_nodes_by_degree_range.return_value = [
        {"id": "node1", "frequency": 10, "relationships": 3},
        {"id": "node2", "frequency": 5, "relationships": 4},
    ]
    mock_instance.get_nodes_by_min_degree.return_value = [
        {"id": "node1", "frequency": 10, "relationships": 4},
    ]
    from NodeConnections.app import app

class TestNodeConnections(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index_route(self):
        """Test that the index path loads correctly."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_get_nodes_by_degree(self):
        """Test for get_nodes_by_degree."""
        degree = 2
        result = mock_instance.get_nodes_by_degree(degree)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["id"], "node1")
        self.assertEqual(result[1]["id"], "node2")

    def test_get_nodes_by_degree_range(self):
        """Test for get_nodes_by_degree_range."""
        min_degree = 3
        max_degree = 5
        result = mock_instance.get_nodes_by_degree_range(min_degree, max_degree)
        self.assertEqual(len(result), 2)
        self.assertIn({"id": "node1", "frequency": 10, "relationships": 3}, result)
        self.assertIn({"id": "node2", "frequency": 5, "relationships": 4}, result)

    def test_get_nodes_by_min_degree(self):
        """Test fora get_nodes_by_min_degree."""
        min_degree = 4
        result = mock_instance.get_nodes_by_min_degree(min_degree)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["id"], "node1")

    def test_close_driver(self):
        """Try to close the controller."""
        mock_instance.close_driver()
        mock_instance.close_driver.assert_called_once()


if __name__ == '__main__':
    unittest.main()
