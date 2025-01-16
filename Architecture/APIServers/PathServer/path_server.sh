#!/bin/bash

# Input
VPC_ID=$1
PRIVATE_SUBNET_ID=$2
NEO4J_HOST="10.0.2.21"
KEY_PAIR_NAME="user"
REGION="us-east-1"
NGINX_SG_NAME="nginx-sg"
PRIVATE_API_SG_NAME="private-api-sg"
PRIVATE_IP="10.0.2.52"
INSTANCE_TYPE="t2.micro"
AMI_ID="ami-01816d07b1128cd2d"
EBS_VOLUME_SIZE=20

if [ -z "$VPC_ID" ] || [ -z "$PRIVATE_SUBNET_ID" ]; then
    echo "Use: $0 <VPC_ID> <PRIVATE_SUBNET_ID>"
    exit 1
fi

# Key Pair
if [ ! -f "./${KEY_PAIR_NAME}.pem" ]; then
    aws ec2 create-key-pair --key-name $KEY_PAIR_NAME --region $REGION --query 'KeyMaterial' --output text > ./${KEY_PAIR_NAME}.pem
    chmod 400 ./${KEY_PAIR_NAME}.pem
fi

# NGINX SG
NGINX_SG_ID=$(aws ec2 describe-security-groups --filters Name=group-name,Values=$NGINX_SG_NAME --query 'SecurityGroups[0].GroupId' --output text 2>/dev/null)

if [ "$NGINX_SG_ID" == "None" ] || [ -z "$NGINX_SG_ID" ]; then
    NGINX_SG_ID=$(aws ec2 create-security-group --group-name $NGINX_SG_NAME --description "Security group for NGINX" --vpc-id $VPC_ID --query 'GroupId' --output text)
    if [ -z "$NGINX_SG_ID" ]; then
        echo "Error creating NGINX security group."
        exit 1
    fi
    aws ec2 authorize-security-group-ingress --group-id $NGINX_SG_ID --protocol tcp --port 8080-8086 --cidr 0.0.0.0/0
    aws ec2 authorize-security-group-ingress --group-id $NGINX_SG_ID --protocol tcp --port 80 --cidr 0.0.0.0/0
    echo "Security group $NGINX_SG_NAME created: $NGINX_SG_ID"
fi

# PRIVATE API SG
API_SG_ID=$(aws ec2 describe-security-groups --filters Name=group-name,Values=$PRIVATE_API_SG_NAME --query 'SecurityGroups[0].GroupId' --output text 2>/dev/null)

if [ "$API_SG_ID" == "None" ] || [ -z "$API_SG_ID" ]; then
    API_SG_ID=$(aws ec2 create-security-group --group-name $PRIVATE_API_SG_NAME --description "Security group for private API servers" --vpc-id $VPC_ID --query 'GroupId' --output text)
    if [ -z "$API_SG_ID" ]; then
        echo "Error creating the PRIVATE API security group."
        exit 1
    fi
    aws ec2 authorize-security-group-ingress --group-id $API_SG_ID --protocol tcp --port 8080-8086 --source-group $NGINX_SG_ID
    echo "Security group $PRIVATE_API_SG_NAME created: $API_SG_ID"
fi

aws ec2 revoke-security-group-ingress --group-id $NGINX_SG_ID --protocol tcp --port 8080-8086 --cidr 0.0.0.0/0 2>/dev/null
aws ec2 authorize-security-group-ingress --group-id $NGINX_SG_ID --protocol tcp --port 8080-8086 --source-group $API_SG_ID
echo "Updated rules for $NGINX_SG_NAME: only traffic from $PRIVATE_API_SG_NAME allowed."

# user-data
cat <<EOF > user-data.sh
#!/bin/bash
sudo yum install -y docker
sudo systemctl start docker
sudo systemctl enable docker
sudo docker pull susanasrez/wordnetnexus-docker:shortest-path-app
sudo docker run -d -p 8080:8080 \
  -e NEO4J_URI="bolt://$NEO4J_HOST:7687" \
  -e NEO4J_USER="neo4j" \
  -e NEO4J_PASSWORD="neo4j" \
  susanasrez/wordnetnexus-docker:shortest-path-app
sudo docker pull susanasrez/wordnetnexus-docker:all-paths-app
sudo docker run -d -p 8081:8081 \
  -e NEO4J_URI="bolt://$NEO4J_HOST:7687" \
  -e NEO4J_USER="neo4j" \
  -e NEO4J_PASSWORD="neo4j" \
  susanasrez/wordnetnexus-docker:all-paths-app
EOF

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
    --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=paths-server}]' \
    --query 'Instances[0].InstanceId' --output text)

if [ -z "$INSTANCE_ID" ]; then
    echo "Error."
    exit 1
fi

aws ec2 wait instance-running --instance-ids $INSTANCE_ID
aws ec2 wait instance-status-ok --instance-ids $INSTANCE_ID
rm -f user-data.sh

#Summary
echo "  Instance ID - Paths Server: $INSTANCE_ID"