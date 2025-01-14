from AllPaths.settings import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD
from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable

class QueryHandler:

    def __init__(self):
        self.driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    
    def find_all_paths(self, start_id, end_id):
        with self.driver.session() as session:
            query = """
            MATCH p = (start:Word {id: $startId})-[:RELATED*..5]-(end:Word {id: $endId})
            RETURN p
            """
            parameters = {
                "startId": start_id,
                "endId": end_id
            }
            try:
                result = session.run(query, parameters)
                paths = [record["p"] for record in result]
                return paths
            except ServiceUnavailable as e:
                print(f"Connection error: {e}")
                return []
