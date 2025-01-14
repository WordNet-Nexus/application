from src.graph_builder.word_checker import WordChecker
from src.graph_builder.builder import Builders
import hazelcast
import config.settings as config
from collections import defaultdict
from itertools import combinations

def process_pair_of_words(couple, word_frequencies):
    word1, word2 = couple
    if WordChecker.are_one_letter_apart(word1, word2):
        weight = (word_frequencies[word1] + word_frequencies[word2]) / 2
        return (word1, word2, weight)
    return None

class NetworkxBuilder(Builders):

    def __init__(self):
        pass

    def process_chunk(self, chunk, word_frequencies):
        aristas = []
        for pareja in chunk:
            resultado = process_pair_of_words(pareja, word_frequencies)
            if resultado:
                aristas.append(resultado)
        return aristas

    @staticmethod
    def chunked_iterable(iterable, chunk_size):
        chunk = []
        for item in iterable:
            chunk.append(item)
            if len(chunk) >= chunk_size:
                yield chunk
                chunk = []
        if chunk:
            yield chunk

    def filter_words(self, word_frequencies):
        filtered_words = defaultdict(list)
        for word in word_frequencies.keys():
            if len(word) > 1:
                filtered_words[len(word)].append(word)
        return filtered_words

    def generate_filtered_combinations(self, grouped_words):
        for length, words in grouped_words.items():
            for combination in combinations(words, 2):
                yield combination
            
            if length + 1 in grouped_words:
                for word1 in words:
                    for word2 in grouped_words[length + 1]:
                        yield (word1, word2)
            if length - 1 in grouped_words:
                for word1 in words:
                    for word2 in grouped_words[length - 1]:
                        yield (word1, word2)

    def create_graph(self, max_workers=None, chunk_size=100000):
        client = hazelcast.HazelcastClient(
            cluster_members=config.HAZELCAST_CLUSTER_MEMBERS,
            cluster_name=config.CLUSTER_NAME
        )
        words_map = client.get_map(config.DICT_NAME).blocking()
        entries = words_map.entry_set()
        word_frequencies = dict(entries)
        client.shutdown()

        grouped_words = self.filter_words(word_frequencies)
        return grouped_words, word_frequencies
