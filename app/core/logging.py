"""Logging setup."""

import logging
import sys

from app.core.request_context import get_request_id


def setup_logging(debug: bool = True) -> None:
    """Configure root logging once for the process."""
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s [request_id=%(request_id)s] %(name)s: %(message)s",
        stream=sys.stdout,
        force=True,
    )

    old_factory = logging.getLogRecordFactory()

    def record_factory(*args, **kwargs):  # type: ignore[no-untyped-def]
        record = old_factory(*args, **kwargs)
        record.request_id = get_request_id() or "-"
        return record

    logging.setLogRecordFactory(record_factory)
