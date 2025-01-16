#!/bin/bash

# Input
VPC_ID=$1
PRIVATE_SUBNET_ID=$2
NEO4J_HOST="10.0.2.21"
KEY_PAIR_NAME="user"
REGION="us-east-1"
PRIVATE_API_SG_NAME="private-api-sg"
PRIVATE_IP="10.0.2.53"
INSTANCE_TYPE="t2.micro"
AMI_ID="ami-01816d07b1128cd2d"
EBS_VOLUME_SIZE=20

if [ -z "$VPC_ID" ] || [ -z "$PRIVATE_SUBNET_ID" ]; then
    echo "Use: $0 <VPC_ID> <PRIVATE_SUBNET_ID>"
    exit 1
fi

# user-data
cat <<EOF > user-data.sh
#!/bin/bash
sudo yum install -y docker
sudo systemctl start docker
sudo systemctl enable docker
sudo docker pull susanasrez/wordnetnexus-docker:strongly-connected-app
sudo docker run -d -p 8082:8082 \
  -e NEO4J_URI="bolt://$NEO4J_HOST:7687" \
  -e NEO4J_USER="neo4j" \
  -e NEO4J_PASSWORD="neo4j" \
  susanasrez/wordnetnexus-docker:strongly-connected-app
sudo docker pull susanasrez/wordnetnexus-docker:node-connections-app
sudo docker run -d -p 8083:8083 \
  -e NEO4J_URI="bolt://$NEO4J_HOST:7687" \
  -e NEO4J_USER="neo4j" \
  -e NEO4J_PASSWORD="neo4j" \
  susanasrez/wordnetnexus-docker:node-connections-app
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
    --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=node-con-server}]' \
    --query 'Instances[0].InstanceId' --output text)

if [ -z "$INSTANCE_ID" ]; then
    echo "Error."
    exit 1
fi

aws ec2 wait instance-running --instance-ids $INSTANCE_ID
aws ec2 wait instance-status-ok --instance-ids $INSTANCE_ID
rm -f user-data.sh

#Summary
echo "  Instance ID - Node-Server: $INSTANCE_ID"