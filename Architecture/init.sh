#!/bin/bash

# Environment: VPC
OUTPUT=$(./MainInfrastructure/environment.sh)

VPC_ID=$(echo "$OUTPUT" | grep "VPC ID:" | awk -F': ' '{print $2}')
PUBLIC_SUBNET_ID=$(echo "$OUTPUT" | grep "Public Subnet ID:" | awk -F': ' '{print $2}')
PRIVATE_SUBNET_ID=$(echo "$OUTPUT" | grep "Private Subnet ID:" | awk -F': ' '{print $2}')

# Mostrar los valores
echo "VPC ID: $VPC_ID"
echo "Public subnet ID: $PUBLIC_SUBNET_ID"
echo "Private subnet ID: $PRIVATE_SUBNET_ID"

# Datalake server: MongoDB
./DatalakeServer/datalake_server.sh $VPC_ID $PRIVATE_SUBNET_ID

# Datamart server: Neo4j
./DatamartServer/datamart_server.sh $VPC_ID $PRIVATE_SUBNET_ID

# Crawler server
./Crawler/crawler.sh $VPC_ID $PUBLIC_SUBNET_ID

# Build the datalake
./DatalakeServer/BuildDatalake/build_datalake_server.sh $VPC_ID $PRIVATE_SUBNET_ID

# API server: Paths-server
./APIServers/PathServer/path_server.sh $VPC_ID $PRIVATE_SUBNET_ID

# Build the datamart
./DatamartServer/BuildDatamart/build_datamart_server.sh $VPC_ID $PRIVATE_SUBNET_ID

# API server: Node-server
./APIServers/NodeConServer/node_server.sh $VPC_ID $PRIVATE_SUBNET_ID

# Build Lambdas- Rol
./APIServers/LambdasServer/BuildLambdas/build_lambdas.sh $VPC_ID $PRIVATE_SUBNET_ID

# API server: LambdasServer
./APIServers/LambdasServer/lambdas_server.sh $VPC_ID $PRIVATE_SUBNET_ID

# API server: NGINX-Proxy
OUTPUT=$(./APIServers/NginxServer/nginx_server.sh $VPC_ID $PUBLIC_SUBNET_ID)
PUBLIC_IP=$(echo "$OUTPUT" | grep "Elastic IP" | awk '{print $NF}')
echo "Elastic IP: $PUBLIC_IP"

#./APIServers/LambdasServer/BuildLambdas/build_lambdas.sh vpc-0c0762f5435874357 subnet-07adc159f24cdae96

