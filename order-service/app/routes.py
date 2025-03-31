from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models import Order, OrderStatus
from app.producer import send_order_event

router = APIRouter()


class OrderRequest(BaseModel):
    item_id: int


@router.post("/orders/")
async def create_order(order_request: OrderRequest, db: AsyncSession = Depends(get_db)):
    # Create an order entry
    new_order = Order(item_id=order_request.item_id, status=OrderStatus.PENDING)
    db.add(new_order)
    await db.commit()
    await db.refresh(new_order)  # Get the latest order details from DB

    # Publish to Kafka
    await send_order_event(new_order.id, new_order.item_id)

    return {"message": "Order placed", "order_id": new_order.id}
