FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt
RUN python -m nltk.downloader punkt punkt_tab stopwords

ENV TEMP_FOLDER=/app/data/documents \
    TABLE_NAME=WordCounts \
    HAZELCAST_CLUSTER_MEMBERS=127.0.0.1:5701 \
    REGION_NAME=us-east-1 \
    BUCKET_NAME=wordnetnexus-gutenberg-ulpgc \
    MONGO_HOST=54.196.154.231 \
    MONGO_PORT=27017

CMD ["python", "main.py"]
