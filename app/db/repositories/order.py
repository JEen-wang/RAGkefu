"""Order repository for exact lookups by business keys."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models import Order


class OrderRepository:
    """Read-focused helpers for order exact-query paths."""

    @staticmethod
    async def get_by_order_no(session: AsyncSession, order_no: str) -> Order | None:
        """Fetch one order with items (and logistics if present)."""
        stmt = (
            select(Order)
            .where(Order.order_no == order_no)
            .options(
                selectinload(Order.items),
                selectinload(Order.logistics),
            )
        )
        return await session.scalar(stmt)
