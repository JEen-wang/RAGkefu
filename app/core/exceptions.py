"""Application-level exceptions."""

from typing import Any


class AppError(Exception):
    """Business error mapped to a stable JSON error response."""

    def __init__(
        self,
        code: int,
        message: str,
        *,
        status_code: int = 400,
        detail: Any = None,
    ) -> None:
        self.code = code
        self.message = message
        self.status_code = status_code
        self.detail = detail
        super().__init__(message)
