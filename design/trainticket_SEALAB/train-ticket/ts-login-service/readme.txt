
rest url:
http://account-login-service:12345/welcome
return String:
"Welcome to [ Account Login Service ] !"

build:
mvn clean package

docker:
docker build -t my/ts-login-service .
docker run -p 12342:12342 --name ts-login-service my/ts-login-service
docker run -p 12342:12342 --name ts-login-service --link register-mongo:mongo-local --link ts-sso-service:ts-sso-service --link ts-verification-code-service:ts-verification-code-service my/ts-login-service


!!!!!notice: please add following lines into /etc/hosts to simulate the network access:
127.0.0.1	account-login-service

