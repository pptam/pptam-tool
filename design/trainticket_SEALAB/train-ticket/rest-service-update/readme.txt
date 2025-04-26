
rest url:
http://localhost:15100/greeting?name=jay
return json:
{"id":2,"content":"Hello, jay!"}

build:
mvn -Dmaven.test.skip=true clean package

docker:
docker build -t my/rest-travel.service-update:1.1.1 .
docker run -p 15100:15100 --restart=always --name rest-travel.service-update my/rest-travel.service-update:1.1.1

docker swarm:
docker tag my/rest-travel.service-update:1.1.1 10.141.212.25:5555/my-rest-travel.service-update:1.1.1
docker push 10.141.212.25:5555/my-rest-travel.service-update:1.1.1
http://10.141.212.25:5555/v2/_catalog
ssh root@10.141.212.22
docker travel.service create \
  --name my-rest-travel.service-update \
  --publish 15100:15100 \
  --network my-network \
  --replicas 3 \
  10.141.212.25:5555/my-rest-travel.service-update:1.1.1
docker travel.service create \
  --name my-rest-travel.service-update \
  --publish 15100:15100 \
  --network my-network \
  --update-delay 10s \
  --update-parallelism 2 \
  --update-failure-action continue \
  --replicas 3 \
  10.141.212.25:5555/my-rest-travel.service-update:1.1.1
10.141.212.22:15100/greeting?name=jay

update:
docker travel.service update --image 10.141.212.25:5555/my-rest-travel.service-update:1.1.1 my-rest-travel.service-update