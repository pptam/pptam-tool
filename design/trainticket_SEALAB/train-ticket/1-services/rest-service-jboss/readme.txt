

build:
docker build --tag=jboss/wildfly-admin .


run:
docker run -d --name wildfly_local -p 8080:8080 -p 9990:9990 -it jboss/wildfly-admin


