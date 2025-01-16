#!/bin/bash

# Environment: VPC
OUTPUT=$(./Architecture/MainInfrastructure/environment.sh)

VPC_ID=$(echo "$OUTPUT" | grep "VPC ID:" | awk -F': ' '{print $2}')
PUBLIC_SUBNET_ID=$(echo "$OUTPUT" | grep "Public Subnet ID:" | awk -F': ' '{print $2}')
PRIVATE_SUBNET_ID=$(echo "$OUTPUT" | grep "Private Subnet ID:" | awk -F': ' '{print $2}')

# Mostrar los valores
echo "VPC ID: $VPC_ID"
echo "Public subnet ID: $PUBLIC_SUBNET_ID"
echo "Private subnet ID: $PRIVATE_SUBNET_ID"

# Datalake server: MongoDB
./Architecture/DatalakeServer/datalake_server.sh $VPC_ID $PRIVATE_SUBNET_ID

# Datamart server: Neo4j
./Architecture/DatamartServer/datamart_server.sh $VPC_ID $PRIVATE_SUBNET_ID

# Crawler server
./Architecture/Crawler/crawler.sh $VPC_ID $PUBLIC_SUBNET_ID

# Build the datalake
./Architecture/DatalakeServer/BuildDatalake/build_datalake_server.sh $VPC_ID $PRIVATE_SUBNET_ID

# API server: Paths-server
./Architecture/APIServers/PathServer/path_server.sh $VPC_ID $PRIVATE_SUBNET_ID

# Build the datamart
./Architecture/DatamartServer/BuildDatamart/build_datamart_server.sh $VPC_ID $PRIVATE_SUBNET_ID

# API server: Node-server
./Architecture/APIServers/NodeConServer/node_server.sh $VPC_ID $PRIVATE_SUBNET_ID

# Build Lambdas- Rol
./Architecture/APIServers/LambdasServer/BuildLambdas/build_lambdas.sh $VPC_ID $PRIVATE_SUBNET_ID

# API server: LambdasServer
./Architecture/APIServers/LambdasServer/lambdas_server.sh $VPC_ID $PRIVATE_SUBNET_ID

# API server: NGINX-Proxy
OUTPUT=$(./Architecture/APIServers/NginxServer/nginx_server.sh $VPC_ID $PUBLIC_SUBNET_ID)
PUBLIC_IP=$(echo "$OUTPUT" | grep "Elastic IP" | awk '{print $NF}')
echo "Elastic IP: $PUBLIC_IP"

