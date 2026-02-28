from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_db
from app.models.promocode import PromoCodeModel

router = APIRouter()


@router.delete("/{promocode_id}")
async def get_promocode(promocode_id: int, db: AsyncSession = Depends(get_async_db)):
    stmt = await db.scalars(select(PromoCodeModel).where(PromoCodeModel.id == promocode_id, PromoCodeModel.is_active.is_(True)))
    promocode = stmt.first()
    if promocode is None:
        raise HTTPException(status_code=404)

    promocode.is_active = False
    await db.commit()
    await db.refresh(promocode)
    return {"status": "success", "message": "Promocode marked as inactive"}

