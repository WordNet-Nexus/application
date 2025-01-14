from abc import ABC, abstractmethod

class Downloader(ABC):

    @abstractmethod
    def download(self, from_path, to_path):
        pass