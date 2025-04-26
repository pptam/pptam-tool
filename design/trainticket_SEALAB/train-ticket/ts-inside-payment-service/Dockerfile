FROM java:8-jre


ADD ./target/ts-inside-payment-service-1.0.jar /app/
CMD ["java", "-Xmx200m", "-jar", "/app/ts-inside-payment-service-1.0.jar"]

EXPOSE 18673