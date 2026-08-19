"""数据库 ORM 模型。"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import JSON, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """SQLAlchemy 声明式基类。"""


class User(Base):
    """用户表。"""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    games: Mapped[list[Game]] = relationship(back_populates="user")


class Game(Base):
    """游戏对局表。"""

    __tablename__ = "games"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="in_progress")
    age_round: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    age_range: Mapped[str] = mapped_column(String(16), nullable=False, default="22-25")
    money: Mapped[int] = mapped_column(Integer, nullable=False, default=50000)
    energy: Mapped[int] = mapped_column(Integer, nullable=False, default=10)
    joy: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    employment_status: Mapped[str] = mapped_column(String(32), nullable=False, default="employed")
    decisions: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    ai_review: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    user: Mapped[User] = relationship(back_populates="games")
