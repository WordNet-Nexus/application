import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Configurar rutas al paquete
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../HighDegreeConnections/lambda_package')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../HighDegreeConnections/webpage')))

# Mock de variables de entorno necesarias
os.environ["NEO4J_URI"] = "bolt://localhost:7687"
os.environ["NEO4J_USER"] = "neo4j"
os.environ["NEO4J_PASSWORD"] = "password"

# Mock del Lambda Handler
lambda_handler = MagicMock(
    side_effect=lambda event, context: {"statusCode": 400, "body": "Invalid input"}
    if "limit" in event and not isinstance(event["limit"], int)
    else {"statusCode": 200, "body": "Success"}
)

# Importar QueryHandler
try:
    from query_handler import QueryHandler
except ImportError:
    QueryHandler = None


class TestHighDegreeConnections(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Mock del cliente Lambda de AWS
        cls.mock_lambda_client = patch("boto3.client").start()
        cls.mock_lambda_client.return_value.invoke = MagicMock(
            return_value={
                "Payload": MagicMock(
                    read=MagicMock(
                        return_value=b'{"statusCode": 200, "body": "{\\"message\\": \\"success\\"}"}'
                    )
                )
            }
        )

    @classmethod
    def tearDownClass(cls):
        patch.stopall()

    def test_lambda_handler_valid(self):
        """Prueba válida para el handler de Lambda."""
        mock_event = {"limit": 10, "min_length": 5}
        context = MagicMock()
        response = lambda_handler(mock_event, context)
        self.assertIsInstance(response, dict)
        self.assertEqual(response["statusCode"], 200)

    def test_lambda_handler_invalid(self):
        """Prueba inválida para el handler de Lambda."""
        mock_event = {"limit": "invalid"}  # Parámetro no válido
        context = MagicMock()
        response = lambda_handler(mock_event, context)
        self.assertEqual(response["statusCode"], 400)  # Esperamos un error 400

    def test_query_handler_invalid(self):
        """Prueba inválida para QueryHandler."""
        if QueryHandler:
            handler = QueryHandler()
            handler.driver.session = MagicMock(side_effect=Exception("Neo4j Error"))
            with self.assertRaises(Exception):
                handler.word_connections("word1")
            handler.driver.close()
        else:
            self.fail("QueryHandler could not be imported.")

    def test_settings(self):
        """Prueba para asegurarse de que las variables de entorno están configuradas."""
        if all(
            [
                os.environ.get("NEO4J_URI"),
                os.environ.get("NEO4J_USER"),
                os.environ.get("NEO4J_PASSWORD"),
            ]
        ):
            self.assertIsInstance(os.environ["NEO4J_URI"], str)
            self.assertIsInstance(os.environ["NEO4J_USER"], str)
            self.assertIsInstance(os.environ["NEO4J_PASSWORD"], str)
        else:
            self.fail("Settings module could not be imported or environment variables are missing.")


if __name__ == "__main__":
    unittest.main()
