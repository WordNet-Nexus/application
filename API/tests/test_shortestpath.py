import unittest
from unittest.mock import patch, MagicMock
from ShortestPath.query_handler import QueryHandler


class TestShortestPath(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Mock del driver de Neo4j
        cls.mock_driver = patch("ShortestPath.query_handler.GraphDatabase.driver").start()
        cls.query_handler = QueryHandler()

    @classmethod
    def tearDownClass(cls):
        patch.stopall()

    def test_delete_existing_graph(self):
        """Prueba para borrar un grafo existente."""
        with patch.object(self.query_handler.driver, "session") as mock_session:
            mock_run = mock_session.return_value.run
            mock_run.return_value = None

            try:
                self.query_handler.delete_existing_graph("wordGraph")
                success = True
            except Exception:
                success = False
            self.assertTrue(success)

    def test_create_graph_projection(self):
        """Prueba para crear una proyección de grafo."""
        with patch.object(self.query_handler.driver, "session") as mock_session:
            mock_run = mock_session.return_value.run
            mock_run.return_value = None

            try:
                self.query_handler.create_graph_projection()
                success = True
            except Exception:
                success = False
            self.assertTrue(success)

    def test_get_ids_valid(self):
        """Prueba para obtener IDs de inicio y fin válidos."""
        with patch.object(self.query_handler, "get_node_id") as mock_get_node_id:
            mock_get_node_id.side_effect = [1, 2]

            start_id, end_id = self.query_handler.get_ids("wordGraph", "word1", "word2")
            self.assertEqual(start_id, 1)
            self.assertEqual(end_id, 2)

    def test_find_shortest_path_empty(self):
        """Prueba para encontrar el camino más corto sin resultados."""
        with patch.object(self.query_handler.driver, "session") as mock_session:
            mock_run = mock_session.return_value.run
            mock_run.return_value = iter([])

            paths = self.query_handler.find_shortest_path("wordGraph", 1, 3)
            self.assertEqual(len(paths), 0)


if __name__ == "__main__":
    unittest.main()
