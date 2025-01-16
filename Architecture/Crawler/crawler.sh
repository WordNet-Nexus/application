#!/bin/bash

# Input
VPC_ID=$1
PUBLIC_SUBNET_ID=$2
AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
AWS_SESSION_TOKEN=${AWS_SESSION_TOKEN}
KEY_PAIR_NAME="crawler"
REGION="us-east-1"
AMI_ID="ami-01816d07b1128cd2d"
INSTANCE_TYPE="t2.micro"
SECURITY_GROUP_NAME="crawler-sg"
EBS_VOLUME_SIZE=20

if [ -z "$VPC_ID" ] || [ -z "$PUBLIC_SUBNET_ID" ]; then
    echo "Use: $0 <VPC_ID> <PUBLIC_SUBNET_ID>"
    exit 1
fi

if [ -z "$AWS_ACCESS_KEY_ID" ] || [ -z "$AWS_SECRET_ACCESS_KEY" ] || [ -z "$AWS_SESSION_TOKEN" ]; then
    echo "AWS credentials are not set. Please export AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, and AWS_SESSION_TOKEN."
    exit 1
fi

# Key pair
if [ -f "./${KEY_PAIR_NAME}.pem" ]; then
    echo "Key pair file already exists. Using existing key."
else
    aws ec2 create-key-pair --key-name $KEY_PAIR_NAME --region $REGION --query 'KeyMaterial' --output text > ./${KEY_PAIR_NAME}.pem
    chmod 400 ./${KEY_PAIR_NAME}.pem
fi

# Security group
SECURITY_GROUP_ID=$(aws ec2 describe-security-groups --filters Name=group-name,Values=$SECURITY_GROUP_NAME --query 'SecurityGroups[0].GroupId' --output text 2>/dev/null)

if [ "$SECURITY_GROUP_ID" == "None" ] || [ -z "$SECURITY_GROUP_ID" ]; then
    SECURITY_GROUP_ID=$(aws ec2 create-security-group --group-name $SECURITY_GROUP_NAME --description "Security group for Gutenberg downloader" --vpc-id $VPC_ID --query 'GroupId' --output text)
fi

RULE_EXISTS=$(aws ec2 describe-security-group-rules \
    --filters "Name=group-id,Values=$SECURITY_GROUP_ID" \
              "Name=ip-protocol,Values=tcp" \
              "Name=from-port,Values=22" \
              "Name=to-port,Values=22" \
              "Name=cidr,Values=0.0.0.0/0" \
    --query 'SecurityGroupRules[0]' --output text)
if [ "$RULE_EXISTS" == "None" ]; then
    aws ec2 authorize-security-group-ingress --group-id $SECURITY_GROUP_ID --protocol tcp --port 22 --cidr 0.0.0.0/0
else
    echo "Ingress rule for port 22 already exists."
fi

# user-data
cat <<EOF > Architecture/user-data.sh
#!/bin/bash
sudo yum install -y docker
sudo systemctl start docker
sudo systemctl enable docker
sudo docker pull susanasrez/wordnetnexus-docker:crawler-app
sudo docker run -d --rm \
  -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
  -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
  -e AWS_SESSION_TOKEN=$AWS_SESSION_TOKEN \
  susanasrez/wordnetnexus-docker:crawler-app wordnetnexus-gutenberg-ulpgc-1 1 200
EOF

# Instance
INSTANCE_ID=$(aws ec2 run-instances \
    --image-id $AMI_ID \
    --count 1 \
    --instance-type $INSTANCE_TYPE \
    --key-name $KEY_PAIR_NAME \
    --security-group-ids $SECURITY_GROUP_ID \
    --subnet-id $PUBLIC_SUBNET_ID \
    --associate-public-ip-address \
    --block-device-mappings '[{"DeviceName":"/dev/xvda","Ebs":{"VolumeSize":'$EBS_VOLUME_SIZE'}}]' \
    --user-data file://Architecture/user-data.sh \
    --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=crawler-server}]' \
    --query 'Instances[0].InstanceId' --output text)
aws ec2 wait instance-running --instance-ids $INSTANCE_ID
aws ec2 wait instance-status-ok --instance-ids $INSTANCE_ID

rm -f Architecture/user-data.sh

PUBLIC_IP=$(aws ec2 describe-instances \
    --instance-ids $INSTANCE_ID \
    --query 'Reservations[0].Instances[0].PublicIpAddress' \
    --output text)

# Summary
echo "  Instance ID - Crawler: $INSTANCE_ID"
