#!/bin/bash
sudo yum install -y docker
sudo systemctl start docker
sudo systemctl enable docker
sudo docker pull susanasrez/wordnetnexus-docker:shortest-path-app
sudo docker run -d -p 8080:8080   -e NEO4J_URI="bolt://10.0.2.21:7687"   -e NEO4J_USER="neo4j"   -e NEO4J_PASSWORD="neo4j"   susanasrez/wordnetnexus-docker:shortest-path-app
sudo docker pull susanasrez/wordnetnexus-docker:all-paths-app
sudo docker run -d -p 8081:8081   -e NEO4J_URI="bolt://10.0.2.21:7687"   -e NEO4J_USER="neo4j"   -e NEO4J_PASSWORD="neo4j"   susanasrez/wordnetnexus-docker:all-paths-app
