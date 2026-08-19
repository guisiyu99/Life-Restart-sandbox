"""认证相关路由。"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from pycore.api import success_response
from src.api.deps import get_current_user
from src.api.exceptions import APIError
from src.db.session import get_db
from src.models.auth import LoginRequest, RegisterRequest
from src.services.auth_service import AuthService

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register")
async def register(body: RegisterRequest, db: AsyncSession = Depends(get_db)) -> Any:
    service = AuthService(db)
    try:
        result = await service.register(body.email, body.password)
    except ValueError as exc:
        if str(exc) == "用户已存在":
            raise APIError(code=4003, message="用户已存在", status_code=400) from exc
        raise APIError(code=4000, message=str(exc), status_code=400) from exc
    return success_response(result.model_dump())


@router.post("/login")
async def login(body: LoginRequest, db: AsyncSession = Depends(get_db)) -> Any:
    service = AuthService(db)
    try:
        result = await service.login(body.email, body.password)
    except ValueError as exc:
        raise APIError(code=4001, message="用户名或密码错误", status_code=401) from exc
    return success_response(result.model_dump())


@router.get("/me")
async def get_me(
    current_user: dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = AuthService(db)
    user = await service.get_user_public(current_user["id"])
    if user is None:
        raise APIError(code=4002, message="Token 无效或过期", status_code=401)
    return success_response(user.model_dump())
