from neo4j import GraphDatabase

class AWSStorageNeo4J():

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def upload_edges(self, edges, batch_size=1000):
        with self.driver.session() as session:
            for i in range(0, len(edges), batch_size):
                batch = edges[i:i + batch_size]
                self._bulk_insert_edges(session, batch)

    def _bulk_insert_edges(self, session, batch):
        cypher = """
        UNWIND $batch AS row
        MERGE (a:Word {id: row.source})
        MERGE (b:Word {id: row.target})
        SET a.frequency = COALESCE(a.frequency, row.source_frequency)
        SET b.frequency = COALESCE(b.frequency, row.target_frequency)
        MERGE (a)-[r:RELATED]-(b)  // Relación no dirigida
        SET r.weight = row.weight
        """
        parameters = {
            "batch": [
                {
                    "source": min(edge[0], edge[1]),
                    "target": max(edge[0], edge[1]),
                    "weight": edge[2],
                    "source_frequency": edge[3],
                    "target_frequency": edge[4]
                }
                for edge in batch
            ]
        }
        session.run(cypher, parameters)

    def upload_nodes_and_edges(self, edges, word_frequencies, batch_size=1000):
        with self.driver.session() as session:
            for i in range(0, len(edges), batch_size):
                batch = edges[i:i + batch_size]
                self._bulk_insert_nodes_and_edges(session, batch, word_frequencies)

    def _bulk_insert_nodes_and_edges(self, session, batch, word_frequencies):
        cypher = """
        UNWIND $batch AS row
        MERGE (a:Word {id: row.source})
        SET a.frequency = COALESCE(a.frequency, row.source_frequency)
        MERGE (b:Word {id: row.target})
        SET b.frequency = COALESCE(b.frequency, row.target_frequency)
        MERGE (a)-[r:RELATED]-(b)  // Relación no dirigida
        SET r.weight = row.weight
        """
        parameters = {
            "batch": [
                {
                    "source": min(edge[0], edge[1]),
                    "target": max(edge[0], edge[1]),
                    "weight": edge[2],
                    "source_frequency": word_frequencies.get(edge[0], 0),
                    "target_frequency": word_frequencies.get(edge[1], 0)
                }
                for edge in batch
            ]
        }
        session.run(cypher, parameters)

    def delete_all_nodes(self):
        with self.driver.session() as session:
            session.write_transaction(self._delete_all_nodes)

    @staticmethod
    def _delete_all_nodes(tx):
        query = "MATCH (n) DETACH DELETE n"
        tx.run(query)
