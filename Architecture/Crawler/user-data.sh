#!/bin/bash
sudo yum install -y docker
sudo systemctl start docker
sudo systemctl enable docker
sudo docker pull susanasrez/wordnetnexus-docker:crawler-app
sudo docker run -d --rm   -e AWS_ACCESS_KEY_ID=ASIATVI3RHUCETEK24F5   -e AWS_SECRET_ACCESS_KEY=ig34lTik/0XL3J23JKfyeDYZDjXuUj8XrOVJOqCB   -e AWS_SESSION_TOKEN=IQoJb3JpZ2luX2VjEL3//////////wEaCXVzLXdlc3QtMiJHMEUCIFl32geePCDWfazwXIHfFt+LnpKwPXL+ZidIo9JJWuE+AiEAiueNnUTztK2P/smamfK29KPyoDXqALaxXSStpE0g0Z0qsQIIpv//////////ARACGgwyNTE4NTAyMTA1NjQiDFwSsXnBjglhZmjI7CqFAvxm31zf7mr5w4csVlanWIml0DaBhVlvq1bd+C7140dg0RcfxgF30fyF5sbMQxeZWqgZadbwKhE1eFnKOXEtnMWdu8J7ktWFCYUqjpjGHTc1WuWesFlN7f5+K5zXv055+VZ6UXNse7gQj76TYCCxTJ8G4GZOwNLS3ROFyw4vi/llvwjk2FpTxSry2sMJerSJgK/sD1rBjtQmyfvygSlSU981zf3Y6THypveN8ZmfybpAZkHFG6CpKpHFrbE9EcqeYcVPqZgw4nzq3K3Ehbja0O7S6kgFIYnVvGMueoOWTbhAFNXDwM+JgpKaTffB2P1ErhPRbZwRhZQa7JWUufLS/1jpj+TDXzDLooS8BjqdAeUL97AYvds402NxnM80cMoa2emTZXLSxkzxKGEpZ9jEyE9FTybMTOFHJEpoYny6kIJcUKVEWyNBrFw17SfKXqaWvDubg46PWrObMwov+7E6M3Y4L2QohNWfpI0X23/+ccbqHnjaNFAJrYDiirricxriRy0/OssrhjiR0LPLvEVFkDr0ROcg/mspvCJokJBHwN4Ycwt3i0Ws+Ey8fI4=   susanasrez/wordnetnexus-docker:crawler-app wordnetnexus-gutenberg-ulpgc-1 1 200
