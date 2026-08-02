"""Refund repository for exact lookups by refund number."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models import Refund


class RefundRepository:
    """Read-focused helpers for refund exact-query paths."""

    @staticmethod
    async def get_by_refund_no(session: AsyncSession, refund_no: str) -> Refund | None:
        """Fetch one refund with related order."""
        stmt = (
            select(Refund)
            .where(Refund.refund_no == refund_no)
            .options(selectinload(Refund.order))
        )
        return await session.scalar(stmt)
