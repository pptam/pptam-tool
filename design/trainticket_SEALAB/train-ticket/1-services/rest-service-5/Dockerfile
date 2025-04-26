FROM java:8-jre


ADD ./target/rest-service-5-0.1.0.jar /app/
CMD ["java", "-Xmx200m", "-jar", "/app/rest-service-5-0.1.0.jar"]

EXPOSE 16005