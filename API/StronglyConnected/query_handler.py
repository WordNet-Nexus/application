from settings import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD
from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable

class QueryHandler:

    def __init__(self):
        self.driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    
    def close_driver(self):
        self.driver.close()

    def detect_clusters(self, algorithm):
        try:
            with self.driver.session() as session:
                graph_exists = session.run(
                    "CALL gds.graph.exists('myGraph') YIELD exists RETURN exists"
                ).single()

                if graph_exists and graph_exists['exists']:
                    session.run("CALL gds.graph.drop('myGraph')")

                session.run(
                    """
                    CALL gds.graph.project(
                        'myGraph',
                        'Word',
                        'RELATED'
                    )
                    """
                )

                if algorithm == 'louvain':
                    result = session.run(
                        """
                        CALL gds.louvain.write(
                            'myGraph',
                            { writeProperty: 'community' }
                        )
                        YIELD communityCount, modularity
                        """
                    )
                    response = [record.data() for record in result]
                elif algorithm == 'wcc':
                    result = session.run(
                        """
                        CALL gds.wcc.write(
                            'myGraph',
                            { writeProperty: 'component' }
                        )
                        YIELD componentCount
                        """
                    )
                    response = [record.data() for record in result]
                else:
                    return None, "Unsupported algorithm. Use 'louvain' or 'wcc'."

            return response, None

        except Exception as e:
            return None, str(e)
    
    def fetch_cluster_results(self, property_key):
        try:
            with self.driver.session() as session:
                result = session.run(
                    f"""
                    MATCH (n:Word)
                    RETURN n.id AS id, n.{property_key} AS cluster
                    ORDER BY n.{property_key}
                    """
                )
                nodes = [record.data() for record in result]
            
            return nodes, None

        except Exception as e:
            return None, str(e)
    
    def get_edges(self, property_key, cluster_id):
        try:
            with self.driver.session() as session:
                result = session.run(
                    f"""
                    MATCH (n:Word)-[r:RELATED]-(m:Word)
                    WHERE n.{property_key} = $cluster
                    RETURN n.id AS source, m.id AS target, r.weight AS weight
                    """,
                    cluster=int(cluster_id)
                )
                edges = [record.data() for record in result]

            return edges, None
        except Exception as e:
            return None, str(e)
