docker:
docker build -t my/ts-sso-service .
docker run -p 12349:12349 --name ts-sso-service my/ts-sso-service
