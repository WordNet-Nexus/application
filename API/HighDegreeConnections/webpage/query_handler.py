import boto3
from settings import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD
from neo4j import GraphDatabase
import json
import os

class QueryHandler:

    def __init__(self):
        aws_region = os.getenv('AWS_REGION', 'us-east-1')
        self.lambda_client = boto3.client('lambda', region_name=aws_region)
        self.driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    
    def invoke_lambda(self, limit: int, min_length: int = None):
        payload = {"limit": limit}
        if min_length is not None:
            payload["min_length"] = min_length

        response = self.lambda_client.invoke(
            FunctionName='HighDegreeNodes',
            InvocationType='RequestResponse',
            Payload=json.dumps(payload)
        )

        payload = response['Payload'].read()
        payload = json.loads(payload)
        body = json.loads(payload['body'])

        return body

    def word_connections(self, word):
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (a:Word {id: $word})-[r:RELATED]->(b:Word)
                RETURN b.id AS connected_word, r.weight AS weight
                """,
                {"word": word}
            )
            return [{"connected_word": record["connected_word"], "weight": record["weight"], "main_word": word} for record in result]
