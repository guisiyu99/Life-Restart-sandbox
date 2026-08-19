"""归档路由。"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from pycore.api import success_response
from src.api.deps import get_current_user
from src.db.session import get_db
from src.services.archive_service import ArchiveService

router = APIRouter(prefix="/api/archives", tags=["archives"])


@router.get("")
async def list_archives(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = ArchiveService(db)
    result = await service.list_archives(current_user["id"], page=page, page_size=page_size)
    return success_response(result.model_dump())


@router.get("/{game_id}")
async def get_archive(
    game_id: int,
    current_user: dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = ArchiveService(db)
    result = await service.get_archive(game_id, current_user["id"])
    return success_response(result.model_dump())
