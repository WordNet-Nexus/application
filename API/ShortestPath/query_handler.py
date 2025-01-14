from settings import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD
from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable

class QueryHandler:

    def __init__(self):
        self.driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    def delete_existing_graph(self, graph_name):
        with self.driver.session() as session:
            try:
                session.run(f"CALL gds.graph.drop('{graph_name}', false)")
            except Exception as e:
                print(f"Error while attempting to delete graph '{graph_name}': {e}")


    def create_graph_projection(self):
        query = """
        CALL gds.graph.project(
            'wordGraph',
            'Word',
            {
                RELATED: {
                    properties: ['weight'],
                    orientation: 'UNDIRECTED'
                }
            }
        )
        """
        with self.driver.session() as session:
            session.run(query)
    
    def get_node_id(self, word):
        query = "MATCH (n:Word {id: $word}) RETURN id(n) AS nodeId"
        with self.driver.session() as session:
            result = session.run(query, {"word": word})
            record = result.single()
            return record["nodeId"] if record else None

    def find_shortest_path(self, graph_name, start_id, end_id):
        query = """
        CALL gds.shortestPath.dijkstra.stream($graphName, {
            sourceNode: $startNode,
            targetNode: $endNode,
            relationshipWeightProperty: 'weight'
        })
        YIELD totalCost, path
        RETURN 
            totalCost, 
            [node IN nodes(path) | node.id] AS nodeIds,
            [rel IN relationships(path) | rel.weight] AS weights
        """
        parameters = {
            "graphName": graph_name,
            "startNode": start_id,
            "endNode": end_id
        }
        with self.driver.session() as session:
            try:
                result = session.run(query, parameters)
                paths = []
                for record in result:
                    paths.append({
                        "nodes": record["nodeIds"],
                        "relationships": record["weights"],
                        "totalCost": record["totalCost"]
                    })
                return paths
            except ServiceUnavailable as e:
                print(f"Connection error: {e}")
                return []
    
    def get_ids(self, graph_name, start_word, end_word):
        self.delete_existing_graph(graph_name)
        self.create_graph_projection()
        start_id = self.get_node_id(start_word)
        end_id = self.get_node_id(end_word)

        return start_id, end_id


