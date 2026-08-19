"""归档相关 Pydantic 模型。"""

from __future__ import annotations

from pydantic import BaseModel


class ArchiveItemPublic(BaseModel):
    id: int
    status: str
    money: int
    energy: int
    joy: int
    ai_review: str | None
    outcome_tags: list[str]
    decision_count: int
    summary: str
    created_at: str
    updated_at: str


class ArchiveListResponse(BaseModel):
    items: list[ArchiveItemPublic]
    total: int
    page: int
    page_size: int


class ArchiveDetailPublic(BaseModel):
    id: int
    status: str
    money: int
    energy: int
    joy: int
    ai_review: str
    outcome_tags: list[str]
    decisions: list
    created_at: str
    updated_at: str
