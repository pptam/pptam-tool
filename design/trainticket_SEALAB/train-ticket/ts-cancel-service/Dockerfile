FROM java:8-jre


ADD ./target/ts-cancel-service-1.0.jar /app/
CMD ["java", "-Xmx200m", "-jar", "/app/ts-cancel-service-1.0.jar"]

EXPOSE 18885