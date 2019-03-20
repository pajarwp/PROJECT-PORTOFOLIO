#!/bin/bash

eval "$(ssh-agent -s)" &&
ssh-add -k ~/.ssh/id_rsa &&
cd /home/ubuntu/PROJECT-PORTOFOLIO
git pull

source ~/.profile
echo "$DOCKERHUB_PASS" | sudo docker login --username $DOCKERHUB_USER --password-stdin
sudo docker stop ecommerce
sudo docker rm ecommerce
sudo docker rmi pajarwp/ecommerce
sudo docker run -d --name ecommerce -p 5555:5555 pajarwp/ecommerce:latest
