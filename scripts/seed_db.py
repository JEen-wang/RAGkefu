"""Idempotent database seed for local demo data."""

from __future__ import annotations

import asyncio
import json
import sys
from datetime import datetime
from pathlib import Path

from sqlalchemy import select

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.db.models import Logistics, LogisticsEvent, Order, OrderItem, Product, Refund
from app.db.session import AsyncSessionLocal

SEED_PATH = ROOT / "data" / "seed" / "sample_orders.json"


async def upsert_products(session, products: list[dict]) -> None:
    for item in products:
        existing = await session.scalar(select(Product).where(Product.sku == item["sku"]))
        if existing:
            existing.name = item["name"]
            existing.price_cents = item["price_cents"]
            existing.stock = item["stock"]
            existing.attrs_json = item.get("attrs_json")
            existing.status = item.get("status", "active")
        else:
            session.add(Product(**item))


async def seed_order(session, payload: dict) -> None:
    order_no = payload["order_no"]
    existing = await session.scalar(select(Order).where(Order.order_no == order_no))
    if existing:
        print(f"skip existing order: {order_no}")
        return

    order = Order(
        order_no=order_no,
        user_id=payload["user_id"],
        status=payload["status"],
        total_cents=payload["total_cents"],
    )
    session.add(order)
    await session.flush()

    for item in payload.get("items", []):
        session.add(
            OrderItem(
                order_id=order.id,
                sku=item["sku"],
                qty=item["qty"],
                price_cents=item["price_cents"],
            )
        )

    logistics_payload = payload.get("logistics")
    if logistics_payload:
        logistics = Logistics(
            tracking_no=logistics_payload["tracking_no"],
            order_id=order.id,
            carrier=logistics_payload.get("carrier", ""),
            status=logistics_payload.get("status", "pending"),
            latest_event=logistics_payload.get("latest_event"),
        )
        session.add(logistics)
        await session.flush()
        for event in logistics_payload.get("events", []):
            session.add(
                LogisticsEvent(
                    logistics_id=logistics.id,
                    event_time=datetime.fromisoformat(event["event_time"]),
                    description=event["description"],
                )
            )

    refund_payload = payload.get("refund")
    if refund_payload:
        session.add(
            Refund(
                refund_no=refund_payload["refund_no"],
                order_id=order.id,
                status=refund_payload.get("status", "pending"),
                amount_cents=refund_payload["amount_cents"],
                reason=refund_payload.get("reason"),
            )
        )

    print(f"seeded order: {order_no}")


async def main() -> None:
    data = json.loads(SEED_PATH.read_text(encoding="utf-8"))
    async with AsyncSessionLocal() as session:
        await upsert_products(session, data.get("products", []))
        for order in data.get("orders", []):
            await seed_order(session, order)
        await session.commit()

    print("seed completed")
    print("demo keys: ORD20260802001 / TQ20260802001 / RF20260802001 / SKU-IPHONE-15")


if __name__ == "__main__":
    asyncio.run(main())
