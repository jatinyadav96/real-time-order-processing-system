import os
import random

from aiokafka import AIOKafkaConsumer
import asyncio
import json
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models import Payment
from app.producer import send_payment_event

KAFKA_BROKER = os.getenv("KAFKA_BROKER")
ORDER_TOPIC = os.getenv("ORDER_TOPIC")


async def process_payment(order_data, db: AsyncSession):
    """Simulates payment processing and updates the database."""
    order_id = order_data["order_id"]
    amount = 100
    status = random.choice(["PAID", "FAILED"])

    # Save payment record in DB
    payment = Payment(order_id=order_id, amount=amount, status=status)
    db.add(payment)
    await db.commit()

    # Publish payment event
    await send_payment_event(order_id, status)


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
