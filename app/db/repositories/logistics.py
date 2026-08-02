"""Logistics repository for exact lookups by tracking number."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models import Logistics


class LogisticsRepository:
    """Read-focused helpers for logistics exact-query paths."""

    @staticmethod
    async def get_by_tracking_no(
        session: AsyncSession, tracking_no: str
    ) -> Logistics | None:
        """Fetch one logistics record with events and related order."""
        stmt = (
            select(Logistics)
            .where(Logistics.tracking_no == tracking_no)
            .options(
                selectinload(Logistics.events),
                selectinload(Logistics.order),
            )
        )
        return await session.scalar(stmt)
