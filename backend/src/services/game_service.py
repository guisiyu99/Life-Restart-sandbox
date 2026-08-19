"""游戏业务逻辑。"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from pycore.core import get_logger
from src.api.exceptions import APIError
from src.db.models import Game
from src.constants.employment import resolve_employment_status
from src.constants.game import annual_salary_for_round
from src.models.game import (
    AdvanceRoundResponse,
    ChoiceRequest,
    ChoiceResponse,
    CreateGameRequest,
    DecisionPublic,
    FinishResultPublic,
    GamePublic,
)
from src.repositories.game_repo import GameRepository
from src.services.ai_service import AIService

logger = get_logger()


def _format_dt(value: datetime | None) -> str:
    if value is None:
        return ""
    if value.tzinfo is None:
        return value.isoformat() + "Z"
    return value.isoformat().replace("+00:00", "Z")


def _compute_outcome_tags(money: int, energy: int, joy: int) -> list[str]:
    if joy >= 8:
        return ["平衡人生", "温暖关系"]
    if money >= 200000:
        return ["事业达人"]
    return ["平凡之路"]


def _fallback_review(money: int, energy: int, joy: int) -> str:
    return (
        f"你走过了完整的人生旅程。最终财富：{money}，精力：{energy}，快乐度：{joy}。"
        "这是属于你的独特人生。"
    )


def game_to_public(game: Game) -> GamePublic:
    return GamePublic(
        id=game.id,
        user_id=game.user_id,
        status=game.status,
        age_round=game.age_round,
        age_range=game.age_range,
        money=game.money,
        energy=game.energy,
        joy=game.joy,
        employment_status=game.employment_status,
        decisions=list(game.decisions or []),
        ai_review=game.ai_review,
        created_at=_format_dt(game.created_at),
        updated_at=_format_dt(game.updated_at),
    )


class GameService:
    def __init__(self, db: AsyncSession) -> None:
        self.repo = GameRepository(db)
        self.ai = AIService()

    async def create_game(self, user_id: int, body: CreateGameRequest | None = None) -> GamePublic:
        payload = body or CreateGameRequest()
        game = await self.repo.create(
            user_id=user_id,
            money=payload.money,
            energy=payload.energy,
            joy=payload.joy,
        )
        logger.info("Game created", game_id=game.id, user_id=user_id)
        return game_to_public(game)

    async def get_game(self, game_id: int, user_id: int) -> GamePublic | None:
        game = await self.repo.get_by_id_for_user(game_id, user_id)
        if game is None:
            return None
        return game_to_public(game)

    def _require_active_game(self, game: Game | None, game_id: int) -> Game:
        if game is None:
            raise APIError(code=4004, message="游戏不存在", status_code=404)
        if game.status == "completed":
            raise APIError(code=4005, message="游戏已完成，无法继续", status_code=400)
        return game

    async def submit_choice(
        self,
        game_id: int,
        user_id: int,
        body: ChoiceRequest,
    ) -> ChoiceResponse:
        game = self._require_active_game(
            await self.repo.get_by_id_for_user(game_id, user_id),
            game_id,
        )

        if body.circle not in ("life", "career"):
            raise APIError(code=4000, message="无效的圈子类型", status_code=400)

        decision = DecisionPublic(
            round=game.age_round,
            age_range=game.age_range,
            circle=body.circle,
            theme=body.theme,
            event_title=body.event_title,
            event_description=body.event_description,
            chosen_option=body.chosen_option_text,
            money_change=body.money_change,
            energy_change=body.energy_change,
            joy_change=body.joy_change,
        )

        new_status = resolve_employment_status(
            current=game.employment_status,  # type: ignore[arg-type]
            theme=body.theme,
            event_title=body.event_title,
            event_description=body.event_description,
            chosen_option=body.chosen_option_text,
        )

        updated = await self.repo.apply_choice(
            game,
            decision=decision.model_dump(),
            money_change=body.money_change,
            energy_change=body.energy_change,
            joy_change=body.joy_change,
            employment_status=new_status,
        )
        logger.info("Choice submitted", game_id=game_id, round=game.age_round)
        public = game_to_public(updated)
        return ChoiceResponse(**public.model_dump(), last_decision=decision)

    async def advance_round(self, game_id: int, user_id: int) -> AdvanceRoundResponse:
        game = self._require_active_game(
            await self.repo.get_by_id_for_user(game_id, user_id),
            game_id,
        )

        if game.age_round >= 8:
            raise APIError(code=4005, message="已是最后一轮", status_code=400)

        updated, income = await self.repo.advance_round(game)
        next_salary = annual_salary_for_round(updated.age_round)
        logger.info(
            "Round advanced",
            game_id=game_id,
            age_round=updated.age_round,
            age_range=updated.age_range,
            round_salary_income=income,
        )
        public = game_to_public(updated)
        return AdvanceRoundResponse(
            **public.model_dump(),
            round_salary_income=income,
            annual_salary=next_salary,
        )

    async def finish_game(
        self,
        game_id: int,
        user_id: int,
    ) -> tuple[FinishResultPublic, int, str]:
        game = await self.repo.get_by_id_for_user(game_id, user_id)
        if game is None:
            raise APIError(code=4004, message="游戏不存在", status_code=404)
        if game.status == "completed":
            raise APIError(code=4005, message="游戏已完成，无法继续", status_code=400)
        if game.age_round < 8:
            raise APIError(code=4000, message="尚未到达最后一轮，无法结束游戏", status_code=400)

        await self.repo.apply_final_round_salary(game)
        game = await self.repo.get_by_id_for_user(game_id, user_id)
        assert game is not None

        decisions = list(game.decisions or [])
        code = 200
        message = "success"
        try:
            ai_review = await self.ai.generate_life_review(
                decisions=decisions,
                money=game.money,
                energy=game.energy,
                joy=game.joy,
            )
        except Exception as exc:
            logger.warning("AI life review failed, using fallback", error_msg=str(exc))
            ai_review = _fallback_review(game.money, game.energy, game.joy)
            code = 5002
            message = "AI 服务调用失败，返回默认总结"

        updated = await self.repo.complete_game(game, ai_review=ai_review)
        result = FinishResultPublic(
            id=updated.id,
            outcome_tags=_compute_outcome_tags(updated.money, updated.energy, updated.joy),
            money=updated.money,
            energy=updated.energy,
            joy=updated.joy,
            ai_review=ai_review,
            decisions=decisions,
        )
        logger.info("Game finished", game_id=game_id, fallback=code == 5002)
        return result, code, message
