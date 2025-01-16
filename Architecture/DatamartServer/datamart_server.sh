#!/bin/bash

# Input
VPC_ID=$1
PRIVATE_SUBNET_ID=$2
PRIVATE_IP="10.0.2.21"
KEY_PAIR_NAME="neo4j"
REGION="us-east-1"
INSTANCE_NAME="datamart-server"
AMI_ID="ami-01816d07b1128cd2d"
INSTANCE_TYPE="t2.medium"
SECURITY_GROUP_NAME="neo4j-sg"
EBS_VOLUME_SIZE=20

if [ -z "$VPC_ID" ] || [ -z "$PRIVATE_SUBNET_ID" ]; then
    echo "Use: $0 <VPC_ID> <PRIVATE_SUBNET_ID>"
    exit 1
fi

# Key pair
aws ec2 create-key-pair --key-name $KEY_PAIR_NAME --region us-east-1 --query 'KeyMaterial' --output text > ./${KEY_PAIR_NAME}.pem
chmod 400 ./${KEY_PAIR_NAME}.pem

# Security group
SECURITY_GROUP_ID=$(aws ec2 describe-security-groups --filters Name=group-name,Values=$SECURITY_GROUP_NAME --query 'SecurityGroups[0].GroupId' --output text 2>/dev/null)

if [ "$SECURITY_GROUP_ID" == "None" ] || [ -z "$SECURITY_GROUP_ID" ]; then
    SECURITY_GROUP_ID=$(aws ec2 create-security-group --group-name $SECURITY_GROUP_NAME --description "Security group for Neo4j server" --vpc-id $VPC_ID --query 'GroupId' --output text)
fi

PRIVATE_SUBNET_CIDR=$(aws ec2 describe-subnets --subnet-ids $PRIVATE_SUBNET_ID --query 'Subnets[0].CidrBlock' --output text)
aws ec2 authorize-security-group-ingress --group-id $SECURITY_GROUP_ID --protocol tcp --port 7474 --cidr $PRIVATE_SUBNET_CIDR || echo "Regla para el puerto 7474 ya existe."
aws ec2 authorize-security-group-ingress --group-id $SECURITY_GROUP_ID --protocol tcp --port 7687 --cidr $PRIVATE_SUBNET_CIDR || echo "Regla para el puerto 7687 ya existe."
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
    --block-device-mappings '[{"DeviceName":"/dev/xvda","Ebs":{"VolumeSize":'$EBS_VOLUME_SIZE'}}]' \
    --user-data file://DatamartServer/user-data.sh \
    --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=datamart-server}]' \
    --query 'Instances[0].InstanceId' --output text)

aws ec2 wait instance-running --instance-ids $INSTANCE_ID
aws ec2 wait instance-status-ok --instance-ids $INSTANCE_ID

# Private IP
PRIVATE_IP=$(aws ec2 describe-instances \
    --instance-ids $INSTANCE_ID \
    --query 'Reservations[0].Instances[0].PrivateIpAddress' \
    --output text)

# Summary
echo "  Instance ID - Datamart: $INSTANCE_ID"