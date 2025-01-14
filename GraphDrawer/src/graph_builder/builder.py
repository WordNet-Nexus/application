from abc import ABC, abstractmethod

class Builders(ABC):

    @abstractmethod
    def create_graph(self, word_frequencies):
        pass
