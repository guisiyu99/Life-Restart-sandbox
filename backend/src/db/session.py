"""数据库会话管理。"""

from __future__ import annotations

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from pycore.core.logger import get_logger
from src.core.config import settings
from src.db.models import Base

logger = get_logger()


def normalize_database_url(raw_url: str) -> str:
    """将 SQLite 相对路径解析为 backend/ 下的绝对路径。"""
    prefix = "sqlite+aiosqlite:///"
    if not raw_url.startswith(prefix):
        return raw_url

    relative_path = raw_url[len(prefix) :]
    if relative_path.startswith("./"):
        relative_path = relative_path[2:]

    backend_root = Path(__file__).resolve().parents[2]
    db_path = (backend_root / relative_path).resolve()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    return f"{prefix}{db_path.as_posix()}"


DATABASE_URL = normalize_database_url(settings.database_url)

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    future=True,
)

async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI 依赖：获取数据库会话。"""
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()


@asynccontextmanager
async def get_db_context() -> AsyncGenerator[AsyncSession, None]:
    """上下文管理器形式的数据库会话。"""
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db() -> None:
    """创建数据库表。"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.run_sync(_migrate_schema)
    logger.info("Database initialized", database_url=DATABASE_URL)


def _migrate_schema(sync_conn) -> None:
    """轻量迁移：为已有 SQLite 库补列。"""
    from sqlalchemy import inspect, text

    inspector = inspect(sync_conn)
    if not inspector.has_table("games"):
        return
    columns = {col["name"] for col in inspector.get_columns("games")}
    if "employment_status" not in columns:
        sync_conn.execute(
            text(
                "ALTER TABLE games ADD COLUMN employment_status VARCHAR(32) NOT NULL DEFAULT 'employed'"
            )
        )


async def close_db() -> None:
    """关闭数据库连接。"""
    await engine.dispose()
    logger.info("Database connection closed")
