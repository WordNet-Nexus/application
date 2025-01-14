FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

ENV HAZELCAST_CLUSTER_MEMBERS=127.0.0.1:5702
ENV CLUSTER_NAME=myGraph
ENV DICT_NAME=word_frequencies
ENV MONGO_HOST=127.0.0.1
ENV MONGO_PORT=27017
ENV COLLECTION_NAME=WordCounts
ENV MONGO_DB_NAME=WordCounts
ENV URI=bolt://localhost:7687
ENV USER=neo4j
ENV NEO4J_PASSWORD=password

CMD ["python", "main.py"]
