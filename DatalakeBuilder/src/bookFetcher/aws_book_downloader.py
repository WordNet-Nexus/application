from DatalakeBuilder.src.bookFetcher.downloader import Downloader
import boto3
import os

class AWSBookDownloader(Downloader):

    def download(self, bucket_name, local_dir):
        print(f"Downloading files from {bucket_name} to {local_dir}")
        s3 = boto3.client('s3')
        paginator = s3.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=bucket_name)

        for page in pages:
            if 'Contents' in page:
                for obj in page['Contents']:
                    s3_key = obj['Key']
                    local_path = os.path.join(local_dir, s3_key)
                    os.makedirs(os.path.dirname(local_path), exist_ok=True)
                    s3.download_file(bucket_name, s3_key, local_path)
                    yield local_path

    def delete_temp_file(self, file_path):
        os.remove(file_path)


