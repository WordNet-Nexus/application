from settings import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD
from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable

class QueryHandler:

    def __init__(self):
        self.driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    def close_driver(self):
        self.driver.close()
    
    def get_nodes_by_degree(self, degree):
        try:
            with self.driver.session() as session:
                result = session.run(
                    """
                    MATCH (n:Word)-[:RELATED]-()
                    WITH n, count(*) AS relationships
                    WHERE relationships = $degree
                    RETURN n.id AS id, n.frequency AS frequency, relationships
                    """,
                    degree=degree
                )
                nodes = [record.data() for record in result]
            
            return nodes
        
        except Exception as e:
            raise Exception(f"Error executing Cypher query: {str(e)}")
    
    def get_nodes_by_degree_range(self, min_degree, max_degree):
        try:
            with self.driver.session() as session:
                result = session.run(
                    """
                    MATCH (n:Word)-[:RELATED]-()
                    WITH n, count(*) AS relationships
                    WHERE relationships >= $min_degree AND relationships <= $max_degree
                    RETURN n.id AS id, n.frequency AS frequency, relationships
                    """,
                    min_degree=min_degree,
                    max_degree=max_degree
                )
                nodes = [record.data() for record in result]
            
            return nodes
        
        except Exception as e:
            raise Exception(f"Error executing Cypher query: {str(e)}")
    
    def get_nodes_by_min_degree(self, min_degree):
        try:
            with self.driver.session() as session:
                result = session.run(
                    """
                    MATCH (n:Word)-[:RELATED]-()
                    WITH n, count(*) AS relationships
                    WHERE relationships >= $min_degree
                    RETURN n.id AS id, n.frequency AS frequency, relationships
                    """,
                    min_degree=min_degree
                )
                nodes = [record.data() for record in result]
            
            return nodes
        
        except Exception as e:
            raise Exception(f"Error executing Cypher query: {str(e)}")


