#!/bin/bash
sudo yum install -y docker
sudo systemctl start docker
sudo systemctl enable docker
sudo docker run -d -p 7474:7474 -p 7687:7687 --name neo4j \
    --user="$(id -u):$(id -g)" \
    -e NEO4J_AUTH=none \
    -e NEO4J_dbms_default__listen__address=0.0.0.0 \
    -e NEO4J_dbms_connector_http_listen__address=0.0.0.0:7474 \
    -e NEO4J_dbms_connector_bolt_listen__address=0.0.0.0:7687 \
    -e NEO4JLABS_PLUGINS='["graph-data-science"]' \
    -e NEO4J_dbms_security_procedures_unrestricted="gds.*,apoc.*" \
    -e NEO4J_dbms_security_procedures_allowlist="gds.*,apoc.*" \
    neo4j:4.4.12