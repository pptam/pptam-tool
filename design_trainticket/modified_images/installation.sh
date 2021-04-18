sudo docker load < ts-preserve-service.tar
sudo docker tag 275c7ce61d50 my-ts-preserve-service:latest

sudo docker load < ts-preserve-other-service.tar 
sudo docker tag 8deb904840be my-ts-preserve-other-service:latest