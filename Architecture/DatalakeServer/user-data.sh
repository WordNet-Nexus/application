#!/bin/bash
yum install -y docker
systemctl start docker
systemctl enable docker
docker run -d -p 27017:27017 --name mongodb mongo:6.0