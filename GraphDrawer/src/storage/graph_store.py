from abc import ABC, abstractmethod

class GraphStore(ABC):

    @abstractmethod
    def load_graph(self):
        pass

