"""Rule-based entity extraction for exact-query routing."""

from __future__ import annotations

import re
from dataclasses import dataclass

_ORDER_RE = re.compile(r"\bORD\d+\b", re.IGNORECASE)
_TRACKING_RE = re.compile(r"\bTQ\d+\b", re.IGNORECASE)
_REFUND_RE = re.compile(r"\bRF\d+\b", re.IGNORECASE)
_SKU_RE = re.compile(r"\bSKU-[A-Z0-9-]+\b", re.IGNORECASE)


@dataclass(frozen=True)
class ExtractedEntities:
    """Business keys found in a user query."""

    order_no: str | None = None
    tracking_no: str | None = None
    refund_no: str | None = None
    sku: str | None = None

    @property
    def has_any(self) -> bool:
        return any((self.order_no, self.tracking_no, self.refund_no, self.sku))


def _first(pattern: re.Pattern[str], text: str, *, upper: bool = False) -> str | None:
    match = pattern.search(text)
    if not match:
        return None
    value = match.group(0)
    return value.upper() if upper else value


def extract_entities(query: str) -> ExtractedEntities:
    """Extract the first hit for each supported business entity type."""
    text = query or ""
    return ExtractedEntities(
        order_no=_first(_ORDER_RE, text, upper=True),
        tracking_no=_first(_TRACKING_RE, text, upper=True),
        refund_no=_first(_REFUND_RE, text, upper=True),
        # Keep SKU casing as matched but normalize prefix to SKU-
        sku=(
            (m := _SKU_RE.search(text))
            and ("SKU-" + m.group(0).split("-", 1)[1].upper())
            or None
        ),
    )
