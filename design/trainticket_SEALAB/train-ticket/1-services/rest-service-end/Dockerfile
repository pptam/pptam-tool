FROM java:8-jre


ADD ./target/rest-service-end-0.1.0.jar /app/
CMD ["java", "-Xmx200m", "-jar", "/app/rest-service-end-0.1.0.jar"]

EXPOSE 16000