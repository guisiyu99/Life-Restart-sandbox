"""认证业务逻辑。"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from pycore.core import get_logger
from src.core.security import create_access_token, hash_password, verify_password
from src.db.models import User
from src.models.auth import AuthTokenResponse, UserPublic
from src.repositories.user_repo import UserRepository

logger = get_logger()


def _format_dt(value: datetime | None) -> str:
    if value is None:
        return ""
    if value.tzinfo is None:
        return value.isoformat() + "Z"
    return value.isoformat().replace("+00:00", "Z")


def _user_public(user: User) -> UserPublic:
    return UserPublic(
        id=user.id,
        email=user.email,
        created_at=_format_dt(user.created_at),
    )


def _auth_response(user: User) -> AuthTokenResponse:
    token = create_access_token(user_id=user.id, email=user.email)
    return AuthTokenResponse(
        access_token=token,
        token_type="bearer",
        user=_user_public(user),
    )


class AuthService:
    """注册、登录。"""

    def __init__(self, db: AsyncSession) -> None:
        self.repo = UserRepository(db)

    async def register(self, email: str, password: str) -> AuthTokenResponse:
        existing = await self.repo.get_by_email(email)
        if existing is not None:
            raise ValueError("用户已存在")
        user = await self.repo.create(email, hash_password(password))
        logger.info("User registered", user_id=user.id)
        return _auth_response(user)

    async def login(self, email: str, password: str) -> AuthTokenResponse:
        user = await self.repo.get_by_email(email)
        if user is None or not verify_password(password, user.password_hash):
            raise ValueError("用户名或密码错误")
        logger.info("User logged in", user_id=user.id)
        return _auth_response(user)

    async def get_user_public(self, user_id: int) -> UserPublic | None:
        user = await self.repo.get_by_id(user_id)
        if user is None:
            return None
        return _user_public(user)
