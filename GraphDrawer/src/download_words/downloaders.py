from src.download_words.aws_words_downloaders import AWSWordsDownloader

class Downloaders:

    __downloaders = {
        "AWSMongoDB": AWSWordsDownloader(),
    }

    @staticmethod
    def initialize_downloader(downloader_name):
        return Downloaders.__downloaders[downloader_name]