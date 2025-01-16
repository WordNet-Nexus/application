#!/bin/bash

# Input
VPC_ID=$1
PRIVATE_SUBNET_ID=$2
KEY_PAIR_NAME="mongo"
REGION="us-east-1"
PRIVATE_IP="10.0.2.20"
INSTANCE_NAME="datalake-server"
AMI_ID="ami-01816d07b1128cd2d"
INSTANCE_TYPE="t2.micro"
SECURITY_GROUP_NAME="mongodb-sg"

if [ -z "$VPC_ID" ] || [ -z "$PRIVATE_SUBNET_ID" ] ; then
    echo "Use: $0 <VPC_ID> <PRIVATE_SUBNET_ID> "
    exit 1
fi


# Key pair
aws ec2 create-key-pair --key-name $KEY_PAIR_NAME --region us-east-1 --query 'KeyMaterial' --output text > ./${KEY_PAIR_NAME}.pem
chmod 400 ./${KEY_PAIR_NAME}.pem

# Security Group
SECURITY_GROUP_ID=$(aws ec2 describe-security-groups --filters Name=group-name,Values=$SECURITY_GROUP_NAME --query 'SecurityGroups[0].GroupId' --output text 2>/dev/null)

if [ "$SECURITY_GROUP_ID" == "None" ] || [ -z "$SECURITY_GROUP_ID" ]; then
    SECURITY_GROUP_ID=$(aws ec2 create-security-group --group-name $SECURITY_GROUP_NAME --description "Security group for MongoDB server" --vpc-id $VPC_ID --query 'GroupId' --output text)
fi

PRIVATE_SUBNET_CIDR=$(aws ec2 describe-subnets --subnet-ids $PRIVATE_SUBNET_ID --query 'Subnets[0].CidrBlock' --output text)
aws ec2 authorize-security-group-ingress --group-id $SECURITY_GROUP_ID --protocol tcp --port 27017 --cidr $PRIVATE_SUBNET_CIDR || echo "Regla para el puerto 27017 ya existe."
aws ec2 authorize-security-group-ingress --group-id $SECURITY_GROUP_ID --protocol tcp --port 22 --cidr $PRIVATE_SUBNET_CIDR || echo "Regla para el puerto 22 ya existe."

# Instance
INSTANCE_ID=$(aws ec2 run-instances \
    --image-id $AMI_ID \
    --count 1 \
    --instance-type $INSTANCE_TYPE \
    --key-name $KEY_PAIR_NAME \
    --security-group-ids $SECURITY_GROUP_ID \
    --subnet-id $PRIVATE_SUBNET_ID \
    --private-ip-address $PRIVATE_IP \
    --user-data file://DatalakeServer/user-data.sh \
    --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=datalake-server}]' \
    --query 'Instances[0].InstanceId' --output text)
aws ec2 wait instance-running --instance-ids $INSTANCE_ID
aws ec2 wait instance-status-ok --instance-ids $INSTANCE_ID

PRIVATE_IP=$(aws ec2 describe-instances \
    --instance-ids $INSTANCE_ID \
    --query 'Reservations[0].Instances[0].PrivateIpAddress' \
    --output text)

# Summary
echo "  Instance ID - Datalake: $INSTANCE_ID"