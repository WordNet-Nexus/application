from src.graph_builder.graph_builder import NetworkxBuilder
from src.storage.aws_storage_neo4j import AWSStorageNeo4J
from src.download_words.downloaders import Downloaders
from config.settings import URI, USER, PASSWORD
from concurrent.futures import ProcessPoolExecutor, as_completed

class Controller:

    @staticmethod
    def initialize(max_workers=None, chunk_size=100000, upload_batch_size=1000):
        downloader = Downloaders.initialize_downloader("AWSMongoDB")
        print("Downloading words from MongoDB and uploading to Hazelcast...")
        downloader.run()
        print("Words have been downloaded and uploaded to Hazelcast.")

        graph_builder = NetworkxBuilder()
        grouped_words, word_frequencies = graph_builder.create_graph()
        print("Graph created.")

        storage = AWSStorageNeo4J(URI, USER, PASSWORD)
        try:
            storage.delete_all_nodes()
            all_combinations = graph_builder.generate_filtered_combinations(grouped_words)
            combinations_generator = graph_builder.chunked_iterable(all_combinations, chunk_size)
            print("All combinations have been generated.")

            print("Processing and uploading edges to Neo4j...")
            for chunk in combinations_generator:
                try:
                    edges = graph_builder.process_chunk(chunk, word_frequencies)
                    if edges:
                        edges_with_frequencies = [
                            (edge[0], edge[1], edge[2], word_frequencies.get(edge[0], 0), word_frequencies.get(edge[1], 0))
                            for edge in edges
                        ]
                        storage.upload_edges(edges_with_frequencies, batch_size=upload_batch_size)
                        print(f"Uploaded {len(edges)} edges to Neo4j.")
                except Exception as e:
                    print(f"Error processing chunk: {e}")

            print("All edges have been processed and uploaded to Neo4j.")

        finally:
            storage.close()
            print("Neo4j connection closed.")
