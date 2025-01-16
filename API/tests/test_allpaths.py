import unittest
from unittest.mock import patch
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

class MockNode:
    def __init__(self, node_id):
        self.id = node_id

    def __getitem__(self, key):
        if key == "id":
            return self.id
        raise KeyError(key)

class MockRelationship:
    def __init__(self, rel_type, start_node, end_node):
        self.type = rel_type
        self.start_node = start_node
        self.end_node = end_node

class MockPath:
    def __init__(self, nodes, relationships):
        self.nodes = nodes
        self.relationships = relationships

with patch('AllPaths.query_handler.QueryHandler') as MockQueryHandler:
    mock_instance = MockQueryHandler.return_value

    node1 = MockNode("word1")
    node2 = MockNode("word2")

    relationship = MockRelationship("RELATED", start_node=node1, end_node=node2)

    mock_path = MockPath(
        nodes=[node1, node2],
        relationships=[relationship]
    )
    mock_instance.find_all_paths.return_value = [mock_path]
    from AllPaths.app import app

class TestAllPaths(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index_post_invalid(self):
        response = self.app.post('/', data={
            'start_word': '',
            'end_word': ''
        })

        self.assertEqual(response.status_code, 302)

    def test_display_route_valid(self):
        response = self.app.get('/display?start_word=word1&end_word=word2')

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'"word1"', response.data)
        self.assertIn(b'"word2"', response.data)

    def test_display_route_invalid(self):
        response = self.app.get('/display?start_word=&end_word=')

        self.assertEqual(response.status_code, 302)

if __name__ == '__main__':
    unittest.main()
