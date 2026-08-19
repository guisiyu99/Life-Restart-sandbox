"""历史档案查询。"""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from src.api.exceptions import APIError
from src.db.models import Game
from src.models.archive import ArchiveDetailPublic, ArchiveItemPublic, ArchiveListResponse
from src.repositories.game_repo import GameRepository
from src.services.game_service import _compute_outcome_tags, _format_dt


def _game_to_archive_item(game: Game) -> ArchiveItemPublic:
    review = game.ai_review or ""
    decisions = list(game.decisions or [])
    return ArchiveItemPublic(
        id=game.id,
        status=game.status,
        money=game.money,
        energy=game.energy,
        joy=game.joy,
        ai_review=game.ai_review,
        outcome_tags=_compute_outcome_tags(game.money, game.energy, game.joy),
        decision_count=len(decisions),
        summary=review[:40] + ("..." if len(review) > 40 else ""),
        created_at=_format_dt(game.created_at),
        updated_at=_format_dt(game.updated_at),
    )


def _game_to_archive_detail(game: Game) -> ArchiveDetailPublic:
    review = game.ai_review or ""
    return ArchiveDetailPublic(
        id=game.id,
        status=game.status,
        money=game.money,
        energy=game.energy,
        joy=game.joy,
        ai_review=review,
        outcome_tags=_compute_outcome_tags(game.money, game.energy, game.joy),
        decisions=list(game.decisions or []),
        created_at=_format_dt(game.created_at),
        updated_at=_format_dt(game.updated_at),
    )


class ArchiveService:
    def __init__(self, db: AsyncSession) -> None:
        self.repo = GameRepository(db)

    async def list_archives(
        self,
        user_id: int,
        *,
        page: int = 1,
        page_size: int = 20,
    ) -> ArchiveListResponse:
        page = max(page, 1)
        page_size = min(max(page_size, 1), 100)
        games, total = await self.repo.list_completed_by_user(
            user_id,
            page=page,
            page_size=page_size,
        )
        return ArchiveListResponse(
            items=[_game_to_archive_item(game) for game in games],
            total=total,
            page=page,
            page_size=page_size,
        )

    async def get_archive(self, game_id: int, user_id: int) -> ArchiveDetailPublic:
        game = await self.repo.get_completed_by_user(game_id, user_id)
        if game is None:
            raise APIError(code=4004, message="归档记录不存在", status_code=404)
        return _game_to_archive_detail(game)
