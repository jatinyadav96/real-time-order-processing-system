# Basic Kafka Commands

## 1️⃣ Start Kafka and Zookeeper (Docker)
Run Kafka and Zookeeper using Docker Compose:
```sh
docker-compose up -d
```
Check running containers:
```sh
docker ps
```

## 2️⃣ Create a Topic
```sh
kafka-topics.sh --create --topic orders --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```
- `orders` → Name of the topic
- `--partitions 1` → Number of partitions
- `--replication-factor 1` → Replication factor (should be <= number of brokers)

## 3️⃣ List All Topics
```sh
kafka-topics.sh --list --bootstrap-server localhost:9092
```

## 4️⃣ Describe a Topic
```sh
kafka-topics.sh --describe --topic orders --bootstrap-server localhost:9092
```

## 5️⃣ Produce Messages to a Topic
```sh
kafka-console-producer.sh --topic orders --bootstrap-server localhost:9092
```
Type messages and press Enter to send them.

## 6️⃣ Consume Messages from a Topic
```sh
kafka-console-consumer.sh --topic orders --bootstrap-server localhost:9092 --from-beginning
```
- `--from-beginning` → Reads all messages from the start.

## 7️⃣ Delete a Topic
```sh
kafka-topics.sh --delete --topic orders --bootstrap-server localhost:9092
```

## 8️⃣ List Consumer Groups
```sh
kafka-consumer-groups.sh --list --bootstrap-server localhost:9092
```

## 9️⃣ Describe a Consumer Group
```sh
kafka-consumer-groups.sh --describe --group my-group --bootstrap-server localhost:9092
```

## 🔟 Delete a Consumer Group
```sh
kafka-consumer-groups.sh --delete --group my-group --bootstrap-server localhost:9092
```