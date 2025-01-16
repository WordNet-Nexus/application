from src.bookFetcher.downloader import Downloader
import boto3
import os

class AWSBookDownloader(Downloader):

    def download(self, bucket_name, local_dir, start_id, end_id):
        print(f"Downloading files from {bucket_name} to {local_dir}")
        s3 = boto3.client('s3')

        for book_id in range(start_id, end_id + 1):
            file_name = f"{book_id}.txt"
            local_path = os.path.join(local_dir, file_name)

            try:
                s3.download_file(bucket_name, file_name, local_path)
                print(f"Downloaded: {file_name}")
                yield local_path
            except s3.exceptions.ClientError as e:
                error_code = int(e.response['Error']['Code'])
                if error_code == 404:
                    print(f"File not found: {file_name}")
                else:
                    print(f"Error downloading {file_name}: {e}")

    def delete_temp_file(self, file_path):
        try:
            os.remove(file_path)
            print(f"Deleted temporary file: {file_path}")
        except FileNotFoundError:
            print(f"File not found when trying to delete: {file_path}")