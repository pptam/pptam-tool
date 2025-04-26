
run:
http://localhost:16006/hello6?cal=66
http://localhost:16006/hello6?cal=96
http://localhost:16006/hello6?cal=136


mvn repo:
https://repo1.maven.org/maven2/


clean images:
docker volume rm $(docker volume ls -qf dangling=true)
docker images|grep none|awk '{print $3 }'|xargs docker rmi


build:
mvn -Dmaven.test.skip=true clean package
docker-compose -f docker-compose.yml build


run:
docker-compose -f docker-compose.yml up -d
docker-compose down
docker-compose logs -f


rest url:
http://localhost:16006/hello6?cal=50
http://rest-service-6:16006/hello6?cal=50


rabbit mq queue:
docker run -d -p 5672:5672 -p 15672:15672 --name rest-service-queue rabbitmq:management
http://localhost:15672


zipkin:
docker run -d -p 9411:9411 --name myzipkin openzipkin/zipkin
http://zipkin:9411/
http://172.16.0.1:9411/
http://10.141.212.25:9411/
traces:
http://localhost:9411/api/v1/traces?annotationQuery=&endTs=1496377639992&limit=100&lookback=3600000&minDuration=&serviceName=rest-service-6&sortOrder=duration-desc&spanName=all
http://localhost:9411/api/v1/traces?annotationQuery=&minDuration=&serviceName=rest-service-6&sortOrder=duration-desc&spanName=all


redis:
docker run -d --name myredis -p 6379:6379 redis


docker ui:
docker run -d -p 9000:9000 --name=portainer-ui-local -v /var/run/docker.sock:/var/run/docker.sock portainer/portainer
http://10.141.212.22:9000/



swarm:

test sample:
http://fdc201705:16006/hello6?cal=66

build:
mvn clean package
docker-compose build
docker tag my-service-cluster/rest-service-end 10.141.212.25:5555/my-rest-service-end
docker tag my-service-cluster/rest-service-1 10.141.212.25:5555/my-rest-service-1
docker tag my-service-cluster/rest-service-2 10.141.212.25:5555/my-rest-service-2
docker tag my-service-cluster/rest-service-3 10.141.212.25:5555/my-rest-service-3
docker tag my-service-cluster/rest-service-4 10.141.212.25:5555/my-rest-service-4
docker tag my-service-cluster/rest-service-5 10.141.212.25:5555/my-rest-service-5
docker tag my-service-cluster/rest-service-6 10.141.212.25:5555/my-rest-service-6
docker tag my-service-cluster/rest-service-go 10.141.212.25:5555/my-rest-service-go
docker tag my-service-cluster/rest-service-nodejs 10.141.212.25:5555/my-rest-service-nodejs
docker tag my-service-cluster/rest-service-python 10.141.212.25:5555/my-rest-service-python

docker push 10.141.212.25:5555/my-rest-service-end
docker push 10.141.212.25:5555/my-rest-service-1
docker push 10.141.212.25:5555/my-rest-service-2
docker push 10.141.212.25:5555/my-rest-service-3
docker push 10.141.212.25:5555/my-rest-service-4
docker push 10.141.212.25:5555/my-rest-service-5
docker push 10.141.212.25:5555/my-rest-service-6
docker push 10.141.212.25:5555/my-rest-service-go
docker push 10.141.212.25:5555/my-rest-service-nodejs
docker push 10.141.212.25:5555/my-rest-service-python

docker stack deploy --compose-file=docker-compose-swarm.yml my-compose-swarm
docker stack ls
docker stack services my-compose-swarm
docker stack ps my-compose-swarm
docker stack rm my-compose-swarm

docker service ls --format "{{.Name}}" | grep "rest-service" | xargs docker service rm
docker service ls --format "{{.Name}}" | xargs docker service rm
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)

docker swarm leave --force
docker node ls
docker node rm 0pvy8v3sugtmcbqualswp1rv5

swarm ui:
http://10.141.211.164:9000/
zipkin:
http://10.141.211.164:9411/



k8s:
kubectl version
kubectl cluster-info
kubectl get nodes
kubectl get clusterroles

### mkdir -p $HOME/.kube
### sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
kubectl create namespace 1-services
kubectl create -f k8s-cluster.yaml
kubectl apply -f k8s-cluster.yaml
kubectl delete -f k8s-cluster.yaml

kubectl get pods --all-namespaces
kubectl get pods -o wide
kubectl get services
kubectl get services -l run=rest-service-1-57d9447f48-76z4d
kubectl describe pods $POD_NAME
kubectl get deployments
kubectl scale deployments/rest-service-6 --replicas=4
kubectl describe services/rest-service-6
kubectl expose deployment/rest-service-6 --type="NodePort" --port 16006

url:
http://fdc201705:32006/hello6?cal=66
http://fdc201705:32411




selenium:
http://www.seleniumhq.org
docker run -d -p 4444:4444 -v /dev/shm:/dev/shm selenium/standalone-chrome:3.4.0-bismuth
10.141.212.21
10.141.212.23
10.141.212.24

monitoring:
ps auxw --sort=%cpu
ps auxw --sort=rss
ps auxw --sort=vsz






