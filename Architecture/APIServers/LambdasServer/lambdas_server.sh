#!/bin/bash

# Input
VPC_ID=$1
PRIVATE_SUBNET_ID=$2
NEO4J_HOST="10.0.2.21"
KEY_PAIR_NAME="user"
REGION="us-east-1"
PRIVATE_API_SG_NAME="private-api-sg"
PRIVATE_IP="10.0.2.54"
INSTANCE_TYPE="t2.micro"
AMI_ID="ami-01816d07b1128cd2d"
EBS_VOLUME_SIZE=20
AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
AWS_SESSION_TOKEN=${AWS_SESSION_TOKEN}

if [ -z "$VPC_ID" ] || [ -z "$PRIVATE_SUBNET_ID" ]; then
    echo "Use: $0 <VPC_ID> <PRIVATE_SUBNET_ID>"
    exit 1
fi

cat <<EOF > user-data.sh
#!/bin/bash
sudo yum install -y docker
sudo systemctl start docker
sudo systemctl enable docker
mkdir -p /root/.aws
cat <<EOC > /root/.aws/credentials
[default]
aws_access_key_id=$AWS_ACCESS_KEY_ID
aws_secret_access_key=$AWS_SECRET_ACCESS_KEY
aws_session_token=$AWS_SESSION_TOKEN
EOC
cat <<EOC > /root/.aws/config
[default]
region=us-east-1
output=json
EOC
sudo docker pull susanasrez/wordnetnexus-docker:high-degree-app
sudo docker run -d -p 8084:8084 \
    -v /root/.aws:/root/.aws:ro \
    -e NEO4J_URI="bolt://$NEO4J_HOST:7687" \
    -e NEO4J_USER="neo4j" \
    -e NEO4J_PASSWORD="neo4j" \
    -e AWS_REGION="us-east-1" \
    susanasrez/wordnetnexus-docker:high-degree-app
sudo docker pull susanasrez/wordnetnexus-docker:isolated-nodes-app
sudo docker run -d -p 8085:8085 \
    -v /root/.aws:/root/.aws:ro \
    -e NEO4J_URI="bolt://$NEO4J_HOST:7687" \
    -e NEO4J_USER="neo4j" \
    -e NEO4J_PASSWORD="neo4j" \
    -e AWS_REGION="us-east-1" \
    susanasrez/wordnetnexus-docker:isolated-nodes-app
sudo docker pull susanasrez/wordnetnexus-docker:max-distance-app
sudo docker run -d -p 8086:8086 \
    -v /root/.aws:/root/.aws:ro \
    -e NEO4J_URI="bolt://$NEO4J_HOST:7687" \
    -e NEO4J_USER="neo4j" \
    -e NEO4J_PASSWORD="neo4j" \
    -e AWS_REGION="us-east-1" \
    susanasrez/wordnetnexus-docker:max-distance-app
EOF

#Security Group
API_SG_ID=$(aws ec2 describe-security-groups \
    --filters "Name=group-name,Values=$PRIVATE_API_SG_NAME" "Name=vpc-id,Values=$VPC_ID" \
    --query 'SecurityGroups[0].GroupId' --output text)

if [ -z "$API_SG_ID" ]; then
    echo "Error"
    exit 1
fi

# Instance
INSTANCE_ID=$(aws ec2 run-instances \
    --image-id $AMI_ID \
    --count 1 \
    --instance-type $INSTANCE_TYPE \
    --key-name $KEY_PAIR_NAME \
    --security-group-ids $API_SG_ID \
    --subnet-id $PRIVATE_SUBNET_ID \
    --private-ip-address $PRIVATE_IP \
    --block-device-mappings '[{"DeviceName":"/dev/xvda","Ebs":{"VolumeSize":'$EBS_VOLUME_SIZE'}}]' \
    --user-data file://user-data.sh \
    --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=lambdas-server}]' \
    --query 'Instances[0].InstanceId' --output text)

if [ -z "$INSTANCE_ID" ]; then
    echo "Error."
    exit 1
fi

aws ec2 wait instance-running --instance-ids $INSTANCE_ID
aws ec2 wait instance-status-ok --instance-ids $INSTANCE_ID
rm -f user-data.sh

#Summary
echo "  Instance ID - Lambdas Server: $INSTANCE_ID"