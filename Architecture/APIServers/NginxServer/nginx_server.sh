#!/bin/bash

# Input
VPC_ID=$1
PUBLIC_SUBNET_ID=$2
KEY_PAIR_NAME="user"
REGION="us-east-1"
NGINX_SG_NAME="nginx-sg"
PUBLIC_IP="10.0.1.6"
INSTANCE_TYPE="t2.micro"
AMI_ID="ami-01816d07b1128cd2d"
EBS_VOLUME_SIZE=20

if [ -z "$VPC_ID" ] || [ -z "$PUBLIC_SUBNET_ID" ]; then
    echo "Use: $0 <VPC_ID> <PUBLIC_SUBNET_ID>"
    exit 1
fi


# Elastic IP
ALLOCATION_ID=$(aws ec2 allocate-address --domain vpc --query 'AllocationId' --output text)
ELASTIC_IP=$(aws ec2 describe-addresses --allocation-ids $ALLOCATION_ID --query 'Addresses[0].PublicIp' --output text)
echo "Elastic IP Reserved: $ELASTIC_IP"

NGINX_SG_ID=$(aws ec2 describe-security-groups \
    --filters "Name=group-name,Values=$NGINX_SG_NAME" \
    --query "SecurityGroups[0].GroupId" \
    --output text)

# user-data
cat <<EOC > Architecture/user-data.sh
#!/bin/bash
sudo yum install -y docker
sudo systemctl start docker
sudo systemcl enable docker
sudo yum install nginx -y
sudo systemctl start nginx
sudo systemctl enable nginx
sudo tee /etc/nginx/conf.d/proxy.conf > /dev/null <<'EOF'
server {
    listen 80;
    server_name $ELASTIC_IP;

    # Página principal
    location / {
        root /usr/share/nginx/html;
        index index.html;
    }

    # Shortest Path App
    location /shortest-path/ {
        proxy_pass http://10.0.2.52:8080/;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    # All Paths App
    location /all-paths/ {
        proxy_pass http://10.0.2.52:8081/;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
    
    # Strongly Connected App
    location /strongly-connected/ {
        proxy_pass http://10.0.2.53:8082/;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
    
    # Node Connections App
    location /node-connections/ {
        proxy_pass http://10.0.2.53:8083/;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
    
    # High Degree Connections
    location /high-degree/ {
        proxy_pass http://10.0.2.54:8084/;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
    
    # Isolated Nodes
    location /isolated-nodes/ {
        proxy_pass http://10.0.2.54:8085/;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
    
    # Max Distance
    location /max-distance/ {
        proxy_pass http://10.0.2.54:8086/;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF
sudo tee /usr/share/nginx/html/index.html > /dev/null <<EOF
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>My Applications</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f2f2f2;
            margin: 0;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: auto;
        }
        h1 {
            text-align: center;
            color: #333;
            margin-bottom: 40px;
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
        }
        .card {
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            padding: 20px;
            text-align: center;
            transition: transform 0.2s;
        }
        .card:hover {
            transform: translateY(-5px);
        }
        .card button {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 12px 20px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
            transition: background-color 0.3s;
            width: 100%;
        }
        .card button:hover {
            background-color: #2ecc71;
        }
        .card p {
            margin-top: 15px;
            color: #555;
            font-size: 14px;
        }
        @media (max-width: 600px) {
            .card button {
                font-size: 14px;
                padding: 10px 16px;
            }
            .card p {
                font-size: 13px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Welcome to WordNet-Nexus Applications</h1>
        <div class="grid">
            <div class="card">
                <button onclick="location.href='/shortest-path/'">Shortest Path</button>
                <p>Find the shortest path between two nodes in a graph.</p>
            </div>
            <div class="card">
                <button onclick="location.href='/all-paths/'">All Paths</button>
                <p>Discover all possible paths between selected nodes.</p>
            </div>
            <div class="card">
                <button onclick="location.href='/strongly-connected/'">Strongly Connected</button>
                <p>Identifying Clusters by detecting densely connected subnetworks.</p>
            </div>
            <div class="card">
                <button onclick="location.href='/node-connections/'">Node Connections</button>
                <p>Analyze connections and relationships between nodes.</p>
            </div>
            <div class="card">
                <button onclick="location.href='/high-degree/'">High Degree Connections</button>
                <p>Find nodes with the highest number of connections.</p>
            </div>
            <div class="card">
                <button onclick="location.href='/isolated-nodes/'">Isolated Nodes</button>
                <p>Identify nodes that have no connections.</p>
            </div>
            <div class="card">
                <button onclick="location.href='/max-distance/'">Max Distance</button>
                <p>Calculate the maximum distance between nodes.</p>
            </div>
        </div>
    </div>
</body>
</html>
EOF
sudo systemctl restart nginx
EOC

# Instance
INSTANCE_ID=$(aws ec2 run-instances \
    --image-id $AMI_ID \
    --count 1 \
    --instance-type $INSTANCE_TYPE \
    --key-name $KEY_PAIR_NAME \
    --security-group-ids $NGINX_SG_ID \
    --subnet-id $PUBLIC_SUBNET_ID \
    --user-data file://Architecture/user-data.sh \
    --block-device-mappings "[{\"DeviceName\":\"/dev/xvda\",\"Ebs\":{\"VolumeSize\":$EBS_VOLUME_SIZE}}]" \
    --query 'Instances[0].InstanceId' \
    --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=nginx-server}]' \
    --output text)

echo "Waiting for the instance to be running..."
aws ec2 wait instance-running --instance-ids $INSTANCE_ID
aws ec2 wait instance-status-ok --instance-ids $INSTANCE_ID
rm -f Architecture/user-data.sh

# Associate Elastic IP
aws ec2 associate-address \
    --instance-id $INSTANCE_ID \
    --allocation-id $ALLOCATION_ID

PUBLIC_IP=$(aws ec2 describe-addresses \
    --allocation-ids $ALLOCATION_ID \
    --query 'Addresses[0].PublicIp' \
    --output text)

echo "Instance ID - NGINX: $INSTANCE_ID"
echo "Elastic IP: $PUBLIC_IP"
