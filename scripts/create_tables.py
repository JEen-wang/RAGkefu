"""Create all ORM tables in the configured database."""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

# Allow `python scripts/create_tables.py` from repo root.
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.db.base import Base
from app.db.session import engine

# Ensure models are registered on Base.metadata before create_all.
import app.db.models  # noqa: F401


async def main() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("tables created (or already exist)")
    print("tables:", ", ".join(sorted(Base.metadata.tables.keys())))


if __name__ == "__main__":
    asyncio.run(main())
