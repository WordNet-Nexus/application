
#!/bin/bash

# Variables
VPC_ID=$1
SUBNET_IDS=$2
ROLE_ARN="arn:aws:iam::398774570408:role/LabRole"
HANDLER="lambda_function.lambda_handler"
PYTHON_RUNTIME="python3.9"
SECURITY_GROUP_NAME="LambdaNeo4jSG"

if [ -z "$VPC_ID" ] || [ -z "$SUBNET_IDS" ] ; then
    echo "Use: $0 <VPC_ID> <PRIVATE_SUBNET_IDS>"
    exit 1
fi

# Security Group
SECURITY_GROUP_ID=$(aws ec2 describe-security-groups \
    --filters Name=group-name,Values=$SECURITY_GROUP_NAME Name=vpc-id,Values=$VPC_ID \
    --query 'SecurityGroups[0].GroupId' \
    --output text 2>/dev/null)

if [ "$SECURITY_GROUP_ID" == "None" ] || [ -z "$SECURITY_GROUP_ID" ]; then
    echo "Security group $SECURITY_GROUP_NAME no existe. Creando..."
    SECURITY_GROUP_ID=$(aws ec2 create-security-group \
        --group-name $SECURITY_GROUP_NAME \
        --description "Security group for Lambda to access Neo4j" \
        --vpc-id $VPC_ID \
        --query 'GroupId' \
        --output text)
    echo "Created Security Group: $SECURITY_GROUP_ID"
    aws ec2 authorize-security-group-egress \
        --group-id "$SECURITY_GROUP_ID" \
        --protocol tcp \
        --port 7687 \
        --cidr 10.0.2.21/32 || echo "Rule already exists"
else
    echo "Security group $SECURITY_GROUP_NAME already exists with ID: $SECURITY_GROUP_ID"
fi

# HighDegreeNodes
LAMBDA_NAME="HighDegreeNodes"
ZIP_FILE="HighDegree/lambda_function.zip"

aws lambda create-function \
    --function-name "$LAMBDA_NAME" \
    --runtime "$PYTHON_RUNTIME" \
    --role "$ROLE_ARN" \
    --handler "$HANDLER" \
    --zip-file fileb://Architecture/APIServers/LambdasServer/BuildLambdas/$ZIP_FILE \
    --vpc-config SubnetIds=$SUBNET_IDS,SecurityGroupIds=$SECURITY_GROUP_ID \
    --environment "Variables={NEO4J_URI=bolt://10.0.2.21:7687,NEO4J_PASSWORD=neo4j,NEO4J_USER=neo4j}"

aws lambda wait function-active --function-name "$LAMBDA_NAME"
echo "$LAMBDA_NAME created"

# Isolated Nodes
LAMBDA_NAME="IsolatedNodes"
ZIP_FILE="Isolated/lambda_function.zip"

aws lambda create-function \
    --function-name "$LAMBDA_NAME" \
    --runtime "$PYTHON_RUNTIME" \
    --role "$ROLE_ARN" \
    --handler "$HANDLER" \
    --zip-file fileb://Architecture/APIServers/LambdasServer/BuildLambdas/$ZIP_FILE \
    --vpc-config SubnetIds=$SUBNET_IDS,SecurityGroupIds=$SECURITY_GROUP_ID \
    --environment "Variables={NEO4J_URI=bolt://10.0.2.21:7687,NEO4J_PASSWORD=neo4j,NEO4J_USER=neo4j}"

aws lambda wait function-active --function-name "$LAMBDA_NAME"
echo "$LAMBDA_NAME created"


# Max Distance
LAMBDA_NAME="MaxDistance"
ZIP_FILE="Max/lambda_function.zip"

aws lambda create-function \
    --function-name "$LAMBDA_NAME" \
    --runtime "$PYTHON_RUNTIME" \
    --role "$ROLE_ARN" \
    --handler "$HANDLER" \
    --zip-file fileb://Architecture/APIServers/LambdasServer/BuildLambdas/$ZIP_FILE \
    --vpc-config SubnetIds=$SUBNET_IDS,SecurityGroupIds=$SECURITY_GROUP_ID \
    --environment "Variables={NEO4J_URI=bolt://10.0.2.21:7687,NEO4J_PASSWORD=neo4j,NEO4J_USER=neo4j}"

aws lambda wait function-active --function-name "$LAMBDA_NAME"
echo "$LAMBDA_NAME created"