"""游戏路由。"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from pycore.api import success_response
from src.api.deps import get_current_user
from src.api.exceptions import APIError
from src.db.session import get_db
from src.models.game import CreateGameRequest, DrawEventRequest, ChoiceRequest
from src.services.event_service import EventService
from src.services.game_service import GameService

router = APIRouter(prefix="/api/games", tags=["games"])


@router.post("")
async def create_game(
    body: CreateGameRequest | None = None,
    current_user: dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = GameService(db)
    game = await service.create_game(current_user["id"], body)
    return success_response(game.model_dump())


@router.get("/{game_id}")
async def get_game(
    game_id: int,
    current_user: dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = GameService(db)
    game = await service.get_game(game_id, current_user["id"])
    if game is None:
        raise APIError(code=4004, message="游戏不存在", status_code=404)
    return success_response(game.model_dump())


@router.post("/{game_id}/draw-event")
async def draw_event(
    game_id: int,
    body: DrawEventRequest | None = None,
    current_user: dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = EventService(db)
    result = await service.draw_event(game_id, current_user["id"], body or DrawEventRequest())
    return success_response(result.model_dump())


@router.post("/{game_id}/choices")
async def submit_choice(
    game_id: int,
    body: ChoiceRequest,
    current_user: dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = GameService(db)
    result = await service.submit_choice(game_id, current_user["id"], body)
    return success_response(result.model_dump())


@router.post("/{game_id}/advance-round")
async def advance_round(
    game_id: int,
    current_user: dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = GameService(db)
    result = await service.advance_round(game_id, current_user["id"])
    return success_response(result.model_dump())


@router.post("/{game_id}/finish")
async def finish_game(
    game_id: int,
    current_user: dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    service = GameService(db)
    result, code, message = await service.finish_game(game_id, current_user["id"])
    return success_response(result.model_dump(), code=code, message=message)
