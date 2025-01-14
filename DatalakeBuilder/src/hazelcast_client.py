import hazelcast

class HazelcastClientManager:
    def __init__(self, cluster_members=["127.0.0.1:5701"]):
        self.client = hazelcast.HazelcastClient(cluster_members=cluster_members)
        self.word_map = self.client.get_map("word_count_map").blocking()

    def get_word_map(self):
        return self.word_map

    def update_word_map(self, word_counts):
        for word, count in word_counts.items():
            current_value = self.word_map.get(word) or 0
            self.word_map.put(word, current_value + count)

    def get_word_map_data(self):
        return {word: count for word, count in self.word_map.entry_set()}

    def shutdown(self):
        self.client.shutdown()
