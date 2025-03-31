import asyncio
import json
import logging
import os

from aiokafka import AIOKafkaConsumer

from app.database import get_consumer_db
from app.models import Order, OrderStatus

KAFKA_BROKER = os.getenv("KAFKA_BROKER")
PAYMENT_TOPIC = os.getenv("PAYMENT_TOPIC")


async def consume_payment_events():
    consumer = AIOKafkaConsumer(
        PAYMENT_TOPIC,
        bootstrap_servers=KAFKA_BROKER,
        group_id="order-service-group",
        auto_offset_reset="earliest"
    )
    await consumer.start()
    try:
        async for message in consumer:
            event = json.loads(message.value.decode("utf-8"))
            order_id = event["order_id"]
            payment_status = event["status"]

            async for db in get_consumer_db():
                await update_order_status(db, order_id, payment_status)
                await db.close()  # Explicitly close the session
                break  # Prevent multiple sessions
    except asyncio.CancelledError:
        print("Consumer stopped.")
    finally:
        await consumer.stop()


async def update_order_status(db, order_id, payment_status):
    try:
        order = await db.get(Order, order_id)
        if order:
            order.status = OrderStatus.PAID if payment_status == "PAID" else OrderStatus.FAILED
            print(f"🔄 Updating order {order_id} to {order.status}")  # Debugging
            # db.add(order)
            await db.flush()  # Ensure the update is staged before commit
            print("🔄 Committing transaction...")
            await db.commit()
            print("✅ Transaction committed!")

        # Verify the update
        await db.refresh(order)
        print(f"✅ Updated Order Status in DB: {order.status}")

    except Exception as e:
        await db.rollback()  # Rollback in case of failure
        print(f"❌ Error updating order {order_id}: {e}")
    finally:
        await db.close()

if __name__ == "__main__":
    try:
        asyncio.run(consume_payment_events())
    except KeyboardInterrupt:
        print("Shutting down consumer...")
