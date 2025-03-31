import os

from aiokafka import AIOKafkaConsumer
import asyncio
import json
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models import Payment

KAFKA_BROKER = os.getenv("KAFKA_BROKER")
ORDER_TOPIC = os.getenv("ORDER_TOPIC")

async def process_payment(order_data, db: AsyncSession):
    """Simulates payment processing and updates the database."""
    order_id = order_data["order_id"]
    amount = 100

    payment = Payment(order_id=order_id, amount=amount, status="SUCCESS")
    db.add(payment)
    await db.commit()

async def consume_orders():
    consumer = AIOKafkaConsumer(
        ORDER_TOPIC,
        bootstrap_servers=KAFKA_BROKER,
        group_id="payment-group",
        auto_offset_reset="earliest"
    )

    await consumer.start()
    try:
        async for msg in consumer:
            order_data = json.loads(msg.value)
            async for db in get_db():
                await process_payment(order_data, db)
    finally:
        await consumer.stop()

if __name__ == "__main__":
    asyncio.run(consume_orders())
