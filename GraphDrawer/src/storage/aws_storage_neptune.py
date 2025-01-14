from src.storage.graph_store import GraphStore
import boto3

class AWSStorageNeptune(GraphStore):

    def __init__(self, graph):
        self.graph = graph

    def load_graph(self):

        client = boto3.client('neptune-data', region_name='us-east-1')
        nodes = []
        edges = []

        for node, data in self.graph.nodes(data=True):
            nodes.append(f"g.addV('word').property('id', '{node}').property('frequency', {data['frequency']})")

        for source, target, data in self.graph.edges(data=True):
            edges.append(f"g.V('{source}').addE('connected').to(g.V('{target}')).property('weight', {data['weight']})")

        for query in nodes + edges:
            response = client.execute_gremlin_query(
                GremlinQuery=query
            )
            print("Response:", response)
