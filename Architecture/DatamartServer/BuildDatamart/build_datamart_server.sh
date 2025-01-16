#!/bin/bash

# Input
VPC_ID=$1
PRIVATE_SUBNET_ID=$2
MONGO_HOST="10.0.2.20"
NEO4J_HOST="10.0.2.21"
PRIVATE_IP="10.0.2.51"
KEY_PAIR_NAME="build"
REGION="us-east-1"
AMI_ID="ami-01816d07b1128cd2d"
INSTANCE_TYPE="t2.medium"
SECURITY_GROUP_NAME="datamart-sg-server"
MONGO_SECURITY_GROUP_NAME="mongo-sg"
EBS_VOLUME_SIZE=30
AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
AWS_SESSION_TOKEN=${AWS_SESSION_TOKEN}

if [ -z "$VPC_ID" ] || [ -z "$PRIVATE_SUBNET_ID" ] ; then
    echo "Use: $0 <VPC_ID> <PRIVATE_SUBNET_ID>"
    exit 1
fi

# Security group
SECURITY_GROUP_ID=$(aws ec2 describe-security-groups --filters Name=group-name,Values=$SECURITY_GROUP_NAME --query 'SecurityGroups[0].GroupId' --output text 2>/dev/null)

if [ "$SECURITY_GROUP_ID" == "None" ] || [ -z "$SECURITY_GROUP_ID" ]; then
    SECURITY_GROUP_ID=$(aws ec2 create-security-group --group-name $SECURITY_GROUP_NAME --description "Security group for Datalake downloader" --vpc-id $VPC_ID --query 'GroupId' --output text)
fi

aws ec2 authorize-security-group-ingress --group-id $SECURITY_GROUP_ID --protocol tcp --port 22 --cidr 0.0.0.0/0 || echo "Rule for port 22 already exists."

# user-data
cat <<EOF > Architecture/user-data-build.sh
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
sudo docker run -d --network host -e HZ_CLUSTERNAME="myGraph" hazelcast/hazelcast
sudo docker pull susanasrez/wordnetnexus-docker:graphdrawer
sudo docker run -d --network host -e HAZELCAST_CLUSTER_MEMBERS="127.0.0.1:5701" \
  -e CLUSTER_NAME="myGraph" \
  -e DICT_NAME="word_frequencies" \
  -e MONGO_HOST=$MONGO_HOST \
  -e MONGO_PORT=27017 \
  -e COLLECTION_NAME="WordCounts" \
  -e MONGO_DB_NAME="WordCounts" \
  -e URI="bolt://$NEO4J_HOST:7687" \
  -e USER="neo4j" \
  -e NEO4J_PASSWORD="neo4j" \
  -v ~/.aws:/root/.aws:ro \
  susanasrez/wordnetnexus-docker:graphdrawer
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
    --user-data file://Architecture/user-data-build.sh \
    --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=build-datamart-server}]' \
    --query 'Instances[0].InstanceId' --output text)

aws ec2 wait instance-running --instance-ids $INSTANCE_ID
aws ec2 wait instance-status-ok --instance-ids $INSTANCE_ID
rm -f Architecture/user-data-build.sh

# Retrieve private IP
PRIVATE_IP=$(aws ec2 describe-instances \
    --instance-ids $INSTANCE_ID \
    --query 'Reservations[0].Instances[0].PrivateIpAddress' \
    --output text)

# Summary
echo "  Instance ID - Build Datamart Server: $INSTANCE_ID"