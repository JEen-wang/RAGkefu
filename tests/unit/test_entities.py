"""Unit tests for rule-based entity extraction."""

from app.services.entities import extract_entities


def test_extract_order_no() -> None:
    entities = extract_entities("帮我查一下订单 ORD20260802001 到哪了")
    assert entities.order_no == "ORD20260802001"
    assert entities.has_any is True


def test_extract_tracking_and_refund() -> None:
    entities = extract_entities("物流 TQ20260802001，退款 RF20260802001")
    assert entities.tracking_no == "TQ20260802001"
    assert entities.refund_no == "RF20260802001"


def test_extract_sku_case_insensitive() -> None:
    entities = extract_entities("这个 sku-iphone-15 有货吗")
    assert entities.sku == "SKU-IPHONE-15"


def test_extract_none() -> None:
    entities = extract_entities("你们的退货政策是什么？")
    assert entities.has_any is False
    assert entities.order_no is None
