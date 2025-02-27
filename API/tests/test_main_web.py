import unittest
from unittest.mock import patch, MagicMock

from main_web.app import app

class TestMainWebApp(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def test_index_route(self):
        """Test the index route"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"<html", response.data)

if __name__ == '__main__':
    unittest.main()
