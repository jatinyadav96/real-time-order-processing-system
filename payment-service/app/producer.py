from aiokafka import AIOKafkaProducer
import json
import os

KAFKA_BROKER = os.getenv("KAFKA_BROKER")
PAYMENT_TOPIC = os.getenv("PAYMENT_TOPIC")


async def send_payment_event(order_id: int, status: str):
    producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BROKER)
    await producer.start()
    try:
        event = {"order_id": order_id, "status": status}
        await producer.send_and_wait(PAYMENT_TOPIC, json.dumps(event).encode("utf-8"))
    finally:
        await producer.stop()
