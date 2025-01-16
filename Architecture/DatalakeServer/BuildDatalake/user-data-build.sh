#!/bin/bash
yum install -y docker
systemctl start docker
systemctl enable docker
mkdir -p /root/.aws
cat <<EOC > /root/.aws/credentials
[default]
aws_access_key_id=ASIATVI3RHUCETEK24F5
aws_secret_access_key=ig34lTik/0XL3J23JKfyeDYZDjXuUj8XrOVJOqCB
aws_session_token=IQoJb3JpZ2luX2VjEL3//////////wEaCXVzLXdlc3QtMiJHMEUCIFl32geePCDWfazwXIHfFt+LnpKwPXL+ZidIo9JJWuE+AiEAiueNnUTztK2P/smamfK29KPyoDXqALaxXSStpE0g0Z0qsQIIpv//////////ARACGgwyNTE4NTAyMTA1NjQiDFwSsXnBjglhZmjI7CqFAvxm31zf7mr5w4csVlanWIml0DaBhVlvq1bd+C7140dg0RcfxgF30fyF5sbMQxeZWqgZadbwKhE1eFnKOXEtnMWdu8J7ktWFCYUqjpjGHTc1WuWesFlN7f5+K5zXv055+VZ6UXNse7gQj76TYCCxTJ8G4GZOwNLS3ROFyw4vi/llvwjk2FpTxSry2sMJerSJgK/sD1rBjtQmyfvygSlSU981zf3Y6THypveN8ZmfybpAZkHFG6CpKpHFrbE9EcqeYcVPqZgw4nzq3K3Ehbja0O7S6kgFIYnVvGMueoOWTbhAFNXDwM+JgpKaTffB2P1ErhPRbZwRhZQa7JWUufLS/1jpj+TDXzDLooS8BjqdAeUL97AYvds402NxnM80cMoa2emTZXLSxkzxKGEpZ9jEyE9FTybMTOFHJEpoYny6kIJcUKVEWyNBrFw17SfKXqaWvDubg46PWrObMwov+7E6M3Y4L2QohNWfpI0X23/+ccbqHnjaNFAJrYDiirricxriRy0/OssrhjiR0LPLvEVFkDr0ROcg/mspvCJokJBHwN4Ycwt3i0Ws+Ey8fI4=
EOC
docker pull susanasrez/wordnetnexus-docker:datalakebuilder
docker run -d --network host hazelcast/hazelcast
docker run -d --rm --network host -p 8000:8000 -e TEMP_FOLDER=/app/data/documents     -e TABLE_NAME=WordCounts     -e HAZELCAST_CLUSTER_MEMBERS=127.0.0.1:5701     -e REGION_NAME=us-east-1     -e BUCKET_NAME=wordnetnexus-gutenberg-ulpgc-1     -e MONGO_HOST=10.0.2.20     -e MONGO_PORT=27017     -v /root/.aws:/root/.aws:ro     --name datalake_container susanasrez/wordnetnexus-docker:datalakebuilder
