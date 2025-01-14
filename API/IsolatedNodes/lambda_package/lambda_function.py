import os
from neo4j import GraphDatabase
import json

def lambda_handler(event, context):
    uri = os.getenv("NEO4J_URI")
    user = os.getenv("NEO4J_USER")
    password = os.getenv("NEO4J_PASSWORD")
    
    driver = GraphDatabase.driver(uri, auth=(user, password))
    try:
        isolated_nodes = query_isolated_nodes(driver)
        return {
            "statusCode": 200,
            "body": json.dumps(isolated_nodes)
        }
    finally:
        driver.close()

def query_isolated_nodes(client):
    with client.session() as session:
        query = """
        MATCH (n)
        WHERE NOT (n)--()
        RETURN n.id AS nodeId
        """
        result = session.run(query)
        return [record["nodeId"] for record in result]
