"""FastAPI 依赖注入。"""

from __future__ import annotations

from typing import Any

import jwt
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.exceptions import APIError
from src.core.config import settings
from src.db.session import get_db
from src.repositories.user_repo import UserRepository

security = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """获取当前登录用户。"""
    if credentials is None or not credentials.credentials:
        raise APIError(code=4002, message="Token 无效或过期", status_code=401)

    token = credentials.credentials
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm],
        )
    except jwt.PyJWTError as exc:
        raise APIError(code=4002, message="Token 无效或过期", status_code=401) from exc

    user_id = payload.get("sub")
    if user_id is None:
        raise APIError(code=4002, message="Token 无效或过期", status_code=401)

    repo = UserRepository(db)
    user = await repo.get_by_id(int(user_id))
    if user is None:
        raise APIError(code=4002, message="Token 无效或过期", status_code=401)

    return {"id": user.id, "email": user.email}
