#!/bin/bash

# Input
VPC_ID=$1
PRIVATE_SUBNET_ID=$2
MONGO_HOST="10.0.2.20"
PRIVATE_IP="10.0.2.50"
KEY_PAIR_NAME="build"
REGION="us-east-1"
AMI_ID="ami-01816d07b1128cd2d"
INSTANCE_TYPE="t2.micro"
SECURITY_GROUP_NAME="datalake-sg-server"
MONGO_SECURITY_GROUP_NAME="mongodb-sg"
EBS_VOLUME_SIZE=20
AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
AWS_SESSION_TOKEN=${AWS_SESSION_TOKEN}

# Validar entradas
if [ -z "$VPC_ID" ] || [ -z "$PRIVATE_SUBNET_ID" ]; then
    echo "Use: $0 <VPC_ID> <PRIVATE_SUBNET_ID>"
    exit 1
fi

if [ -z "$AWS_ACCESS_KEY_ID" ] || [ -z "$AWS_SECRET_ACCESS_KEY" ] || [ -z "$AWS_SESSION_TOKEN" ]; then
    echo "AWS credentials are not set. Please export AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, and AWS_SESSION_TOKEN."
    exit 1
fi

# Validar credenciales AWS
if [ -z "$AWS_ACCESS_KEY_ID" ] || [ -z "$AWS_SECRET_ACCESS_KEY" ]; then
    echo "Error: AWS credentials are not configured."
    exit 1
fi

# Key pair
aws ec2 create-key-pair --key-name $KEY_PAIR_NAME --region $REGION --query 'KeyMaterial' --output text > ./${KEY_PAIR_NAME}.pem
chmod 400 ./${KEY_PAIR_NAME}.pem

# Security group
SECURITY_GROUP_ID=$(aws ec2 describe-security-groups --filters Name=group-name,Values=$SECURITY_GROUP_NAME --query 'SecurityGroups[0].GroupId' --output text 2>/dev/null)

if [ -z "$SECURITY_GROUP_ID" ] || [ "$SECURITY_GROUP_ID" == "None" ]; then
    SECURITY_GROUP_ID=$(aws ec2 create-security-group --group-name $SECURITY_GROUP_NAME \
        --description "Security group for Datalake downloader" --vpc-id $VPC_ID --query 'GroupId' --output text)
fi

aws ec2 authorize-security-group-ingress --group-id $SECURITY_GROUP_ID --protocol tcp --port 22 --cidr 0.0.0.0/0 || echo "Rule for SSH already exists."

# Mongo security group
MONGO_SECURITY_GROUP_ID=$(aws ec2 describe-security-groups --filters Name=group-name,Values=$MONGO_SECURITY_GROUP_NAME --query 'SecurityGroups[0].GroupId' --output text 2>/dev/null)

if [ -z "$MONGO_SECURITY_GROUP_ID" ] || [ "$MONGO_SECURITY_GROUP_ID" == "None" ]; then
    echo "Error: Mongo security group '$MONGO_SECURITY_GROUP_NAME' does not exist."
    exit 1
fi

aws ec2 authorize-security-group-ingress --group-id $MONGO_SECURITY_GROUP_ID --protocol tcp --port 27017 --cidr ${PRIVATE_IP}/32 || echo "Rule to Private Subnet ${PRIVATE_IP} already exists."

# User-data script
cat <<EOF > user-data-build.sh
#!/bin/bash
yum install -y docker
systemctl start docker
systemctl enable docker
mkdir -p /root/.aws
cat <<EOC > /root/.aws/credentials
[default]
aws_access_key_id=$AWS_ACCESS_KEY_ID
aws_secret_access_key=$AWS_SECRET_ACCESS_KEY
aws_session_token=$AWS_SESSION_TOKEN
EOC
docker pull susanasrez/wordnetnexus-docker:datalakebuilder
docker run -d --network host hazelcast/hazelcast
docker run -d --rm --network host -p 8000:8000 -e TEMP_FOLDER=/app/data/documents \
    -e TABLE_NAME=WordCounts \
    -e HAZELCAST_CLUSTER_MEMBERS=127.0.0.1:5701 \
    -e REGION_NAME=us-east-1 \
    -e BUCKET_NAME=wordnetnexus-gutenberg-ulpgc-2 \
    -e MONGO_HOST=$MONGO_HOST \
    -e MONGO_PORT=27017 \
    -v /root/.aws:/root/.aws:ro \
    --name datalake_container susanasrez/wordnetnexus-docker:datalakebuilder
EOF

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
    --user-data file://user-data-build.sh \
    --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=build-datalake-server}]' \
    --query 'Instances[0].InstanceId' --output text)

aws ec2 wait instance-running --instance-ids $INSTANCE_ID
aws ec2 wait instance-status-ok --instance-ids $INSTANCE_ID
rm -f user-data-build.sh

# Summary
echo "  Instance ID - Build Datalake Server: $INSTANCE_ID"
