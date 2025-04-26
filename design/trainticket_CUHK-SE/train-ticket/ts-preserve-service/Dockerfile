FROM openjdk:8-jre
WORKDIR /app
RUN /bin/cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' >/etc/timezone
COPY ./target/*.jar app.jar
EXPOSE 8080
CMD ["java", "-Xmx200m",  "-jar", "app.jar"]
