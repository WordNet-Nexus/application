from src.bookFetcher.aws_book_downloader import AWSBookDownloader

class BookFetcher:

    __downloaders = {
        "AWS": AWSBookDownloader(),
    }

    @staticmethod
    def initialize_downloader(downloader_name):
        return BookFetcher.__downloaders[downloader_name]