
build:
mvn clean package -Dmaven.test.skip=true

mvn run:
mvn exec:java -Dexec.mainClass="example.RemoteDriverTest2"
java -jar target/sample-test-1-1.0.jar

test:
mvn test
mvn test -Dtest=example.Test1
mvn test -Dtest=example.Test1#test1

remote driver:
docker run -d -p 4444:4444 --name selenium-standalone-chrome -v /dev/shm:/dev/shm selenium/standalone-chrome
mvn exec:java -Dexec.mainClass="example.RemoteDriverTest2"

