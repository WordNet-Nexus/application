#!/bin/bash
sudo yum install -y docker
sudo systemctl start docker
sudo systemctl enable docker
mkdir -p /root/.aws
cat <<EOC > /root/.aws/credentials
[default]
aws_access_key_id=ASIATVI3RHUCETEK24F5
aws_secret_access_key=ig34lTik/0XL3J23JKfyeDYZDjXuUj8XrOVJOqCB
aws_session_token=IQoJb3JpZ2luX2VjEL3//////////wEaCXVzLXdlc3QtMiJHMEUCIFl32geePCDWfazwXIHfFt+LnpKwPXL+ZidIo9JJWuE+AiEAiueNnUTztK2P/smamfK29KPyoDXqALaxXSStpE0g0Z0qsQIIpv//////////ARACGgwyNTE4NTAyMTA1NjQiDFwSsXnBjglhZmjI7CqFAvxm31zf7mr5w4csVlanWIml0DaBhVlvq1bd+C7140dg0RcfxgF30fyF5sbMQxeZWqgZadbwKhE1eFnKOXEtnMWdu8J7ktWFCYUqjpjGHTc1WuWesFlN7f5+K5zXv055+VZ6UXNse7gQj76TYCCxTJ8G4GZOwNLS3ROFyw4vi/llvwjk2FpTxSry2sMJerSJgK/sD1rBjtQmyfvygSlSU981zf3Y6THypveN8ZmfybpAZkHFG6CpKpHFrbE9EcqeYcVPqZgw4nzq3K3Ehbja0O7S6kgFIYnVvGMueoOWTbhAFNXDwM+JgpKaTffB2P1ErhPRbZwRhZQa7JWUufLS/1jpj+TDXzDLooS8BjqdAeUL97AYvds402NxnM80cMoa2emTZXLSxkzxKGEpZ9jEyE9FTybMTOFHJEpoYny6kIJcUKVEWyNBrFw17SfKXqaWvDubg46PWrObMwov+7E6M3Y4L2QohNWfpI0X23/+ccbqHnjaNFAJrYDiirricxriRy0/OssrhjiR0LPLvEVFkDr0ROcg/mspvCJokJBHwN4Ycwt3i0Ws+Ey8fI4=
EOC
cat <<EOC > /root/.aws/config
[default]
region=us-east-1
output=json
EOC
sudo docker pull susanasrez/wordnetnexus-docker:high-degree-app
sudo docker run -d -p 8084:8084     -v /root/.aws:/root/.aws:ro     -e NEO4J_URI="bolt://10.0.2.21:7687"     -e NEO4J_USER="neo4j"     -e NEO4J_PASSWORD="neo4j"     -e AWS_REGION="us-east-1"     susanasrez/wordnetnexus-docker:high-degree-app
sudo docker pull susanasrez/wordnetnexus-docker:isolated-nodes-app
sudo docker run -d -p 8085:8085     -v /root/.aws:/root/.aws:ro     -e NEO4J_URI="bolt://10.0.2.21:7687"     -e NEO4J_USER="neo4j"     -e NEO4J_PASSWORD="neo4j"     -e AWS_REGION="us-east-1"     susanasrez/wordnetnexus-docker:isolated-nodes-app
sudo docker pull susanasrez/wordnetnexus-docker:max-distance-app
sudo docker run -d -p 8086:8086     -v /root/.aws:/root/.aws:ro     -e NEO4J_URI="bolt://10.0.2.21:7687"     -e NEO4J_USER="neo4j"     -e NEO4J_PASSWORD="neo4j"     -e AWS_REGION="us-east-1"     susanasrez/wordnetnexus-docker:max-distance-app
