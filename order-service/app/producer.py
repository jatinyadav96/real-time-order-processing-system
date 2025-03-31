from aiokafka import AIOKafkaProducer
import os
from dotenv import load_dotenv
import json

load_dotenv()
KAFKA_BROKER = os.getenv("KAFKA_BROKER")

async def send_order_event(order_id: int, item_id: int):
    producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BROKER)
    await producer.start()
    try:
        message = {"order_id": order_id, "item_id": item_id, "status": "PENDING"}
        await producer.send_and_wait("orders", json.dumps(message).encode("utf-8"))
    finally:
        await producer.stop()
