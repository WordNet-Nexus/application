import unittest
from unittest.mock import patch
import sys
import os

# Asegurar que el directorio raíz del proyecto está en sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

# Clases simuladas para nodos y relaciones
class MockNode:
    def __init__(self, node_id):
        self.id = node_id

    # Permitir acceso como un diccionario
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

# Mockear QueryHandler antes de importar app
with patch('AllPaths.query_handler.QueryHandler') as MockQueryHandler:
    mock_instance = MockQueryHandler.return_value

    # Crear nodos simulados
    node1 = MockNode("word1")
    node2 = MockNode("word2")

    # Crear una relación simulada entre nodos
    relationship = MockRelationship("RELATED", start_node=node1, end_node=node2)

    # Crear un mock para path con nodos y relaciones
    mock_path = MockPath(
        nodes=[node1, node2],
        relationships=[relationship]
    )
    mock_instance.find_all_paths.return_value = [mock_path]
    from AllPaths.app import app

class TestAllPaths(unittest.TestCase):

    def setUp(self):
        # Configurar la aplicación de Flask para pruebas
        self.app = app.test_client()
        self.app.testing = True

    def test_index_post_invalid(self):
        # Probar el caso de datos incompletos
        response = self.app.post('/', data={
            'start_word': '',
            'end_word': ''
        })

        self.assertEqual(response.status_code, 302)  # Redirección esperada

    def test_display_route_valid(self):
        response = self.app.get('/display?start_word=word1&end_word=word2')

        self.assertEqual(response.status_code, 200)
        # Verificar que los datos renderizados contienen el nodo esperado
        self.assertIn(b'"word1"', response.data)
        self.assertIn(b'"word2"', response.data)

    def test_display_route_invalid(self):
        # Probar el caso de parámetros incompletos
        response = self.app.get('/display?start_word=&end_word=')

        self.assertEqual(response.status_code, 302)  # Redirección esperada

if __name__ == '__main__':
    unittest.main()
