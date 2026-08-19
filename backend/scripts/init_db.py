"""初始化 SQLite 数据库表。"""

from __future__ import annotations

import asyncio

from src.db.session import init_db


async def main() -> None:
    await init_db()
    print("Database initialized successfully.")


if __name__ == "__main__":
    asyncio.run(main())
