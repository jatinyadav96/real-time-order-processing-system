from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models import Payment

router = APIRouter()

@router.get("/payments/{order_id}")
async def get_payment_status(order_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Payment).filter(Payment.order_id == order_id))
    payment = result.scalars().first()

    if not payment:
        return {"status": "NOT_FOUND"}

    return {"order_id": order_id, "status": payment.status}
