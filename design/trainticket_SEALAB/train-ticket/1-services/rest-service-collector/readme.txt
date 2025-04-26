

kafka:
docker run -d --name mykafka -p 2181:2181 -p 9092:9092 --env ADVERTISED_HOST=127.0.0.1 --env ADVERTISED_PORT=9092 spotify/kafka
/opt/kafka_2.11-0.10.1.0/bin/kafka-topics.sh --list --zookeeper 127.0.0.1:2181
/opt/kafka_2.11-0.10.1.0/bin/kafka-console-consumer.sh --zookeeper 127.0.0.1:2181 --topic app_log --from-beginning


