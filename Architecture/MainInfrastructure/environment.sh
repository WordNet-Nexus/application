#!/bin/bash

# Variables
CIDR_BLOCK_VPC="10.0.0.0/16"
CIDR_BLOCK_PUBLIC_SUBNET="10.0.1.0/24"
CIDR_BLOCK_PRIVATE_SUBNET="10.0.2.0/24"
AVAILABILITY_ZONE="us-east-1a"
VPC_NAME="MyVPC"

# Create VPC
VPC_ID=$(aws ec2 create-vpc --cidr-block $CIDR_BLOCK_VPC --query 'Vpc.VpcId' --output text)
aws ec2 create-tags --resources $VPC_ID --tags Key=Name,Value=$VPC_NAME
aws ec2 modify-vpc-attribute --vpc-id $VPC_ID --enable-dns-support
aws ec2 modify-vpc-attribute --vpc-id $VPC_ID --enable-dns-hostnames

# Create Public Subnet
PUBLIC_SUBNET_ID=$(aws ec2 create-subnet --vpc-id $VPC_ID --cidr-block $CIDR_BLOCK_PUBLIC_SUBNET --availability-zone $AVAILABILITY_ZONE --query 'Subnet.SubnetId' --output text)

# Create Private Subnet
PRIVATE_SUBNET_ID=$(aws ec2 create-subnet --vpc-id $VPC_ID --cidr-block $CIDR_BLOCK_PRIVATE_SUBNET --availability-zone $AVAILABILITY_ZONE --query 'Subnet.SubnetId' --output text)

# Internet Gateway
IGW_ID=$(aws ec2 create-internet-gateway --query 'InternetGateway.InternetGatewayId' --output text)

# Attach Internet Gateway to VPC
aws ec2 attach-internet-gateway --internet-gateway-id $IGW_ID --vpc-id $VPC_ID

# Create Route Table for Public Subnet
ROUTE_TABLE_PUBLIC_ID=$(aws ec2 create-route-table --vpc-id $VPC_ID --query 'RouteTable.RouteTableId' --output text)

# Create Route to Internet Gateway
aws ec2 create-route --route-table-id $ROUTE_TABLE_PUBLIC_ID --destination-cidr-block 0.0.0.0/0 --gateway-id $IGW_ID

# Associate Public Subnet with Route Table
aws ec2 associate-route-table --route-table-id $ROUTE_TABLE_PUBLIC_ID --subnet-id $PUBLIC_SUBNET_ID

# Public Subnet Configuration
aws ec2 modify-subnet-attribute --subnet-id $PUBLIC_SUBNET_ID --map-public-ip-on-launch

# Create an Elastic IP for NAT Gateway
EIP_ALLOCATION_ID=$(aws ec2 allocate-address --query 'AllocationId' --output text)

# Create NAT Gateway in Public Subnet
NAT_GW_ID=$(aws ec2 create-nat-gateway --subnet-id $PUBLIC_SUBNET_ID --allocation-id $EIP_ALLOCATION_ID --query 'NatGateway.NatGatewayId' --output text)

# Wait for NAT Gateway to become available
echo "Waiting for NAT Gateway to become available..."
aws ec2 wait nat-gateway-available --nat-gateway-ids $NAT_GW_ID

# Create Route Table for Private Subnet
ROUTE_TABLE_PRIVATE_ID=$(aws ec2 create-route-table --vpc-id $VPC_ID --query 'RouteTable.RouteTableId' --output text)

# Create Route in Private Route Table for Internet Access via NAT Gateway
aws ec2 create-route --route-table-id $ROUTE_TABLE_PRIVATE_ID --destination-cidr-block 0.0.0.0/0 --nat-gateway-id $NAT_GW_ID

# Associate Private Subnet with Private Route Table
aws ec2 associate-route-table --route-table-id $ROUTE_TABLE_PRIVATE_ID --subnet-id $PRIVATE_SUBNET_ID

# Summary
echo "VPC ID: $VPC_ID"
echo "Public Subnet ID: $PUBLIC_SUBNET_ID"
echo "Private Subnet ID: $PRIVATE_SUBNET_ID"

# GitHub Actions
echo "::set-output name=vpc_id::$VPC_ID"
echo "::set-output name=public_subnet_id::$PUBLIC_SUBNET_ID"
echo "::set-output name=private_subnet_id::$PRIVATE_SUBNET_ID"

