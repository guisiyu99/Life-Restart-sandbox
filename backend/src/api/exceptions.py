"""API 层异常定义。"""

from __future__ import annotations


class APIError(Exception):
    """契约统一错误格式。"""

    def __init__(self, code: int, message: str, status_code: int = 400) -> None:
        self.code = code
        self.message = message
        self.status_code = status_code
        super().__init__(message)
