"""游戏数据访问层。"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.constants.game import AGE_RANGES, DEFAULT_ENERGY, DEFAULT_JOY, DEFAULT_MONEY, round_salary_income
from src.db.models import Game


class GameRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create(
        self,
        *,
        user_id: int,
        money: int = DEFAULT_MONEY,
        energy: int = DEFAULT_ENERGY,
        joy: int = DEFAULT_JOY,
    ) -> Game:
        game = Game(
            user_id=user_id,
            status="in_progress",
            age_round=1,
            age_range=AGE_RANGES[1],
            money=money,
            energy=energy,
            joy=joy,
            employment_status="employed",
            decisions=[],
            ai_review=None,
        )
        self.db.add(game)
        await self.db.commit()
        await self.db.refresh(game)
        return game

    async def get_by_id(self, game_id: int) -> Game | None:
        result = await self.db.execute(select(Game).where(Game.id == game_id))
        return result.scalar_one_or_none()

    async def get_by_id_for_user(self, game_id: int, user_id: int) -> Game | None:
        result = await self.db.execute(
            select(Game).where(Game.id == game_id, Game.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def list_completed_by_user(
        self,
        user_id: int,
        *,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[list[Game], int]:
        from sqlalchemy import func

        filters = (Game.user_id == user_id, Game.status == "completed")
        count_result = await self.db.execute(
            select(func.count()).select_from(Game).where(*filters)
        )
        total = int(count_result.scalar_one())

        offset = max(page - 1, 0) * page_size
        result = await self.db.execute(
            select(Game)
            .where(*filters)
            .order_by(Game.updated_at.desc())
            .offset(offset)
            .limit(page_size)
        )
        return list(result.scalars().all()), total

    async def get_completed_by_user(self, game_id: int, user_id: int) -> Game | None:
        result = await self.db.execute(
            select(Game).where(
                Game.id == game_id,
                Game.user_id == user_id,
                Game.status == "completed",
            )
        )
        return result.scalar_one_or_none()

    async def apply_choice(
        self,
        game: Game,
        *,
        decision: dict,
        money_change: int,
        energy_change: int,
        joy_change: int,
        employment_status: str | None = None,
    ) -> Game:
        decisions = list(game.decisions or [])
        decisions.append(decision)
        game.decisions = decisions
        game.money = game.money + money_change
        game.energy = max(0, game.energy + energy_change)
        game.joy = max(0, game.joy + joy_change)
        if employment_status is not None:
            game.employment_status = employment_status
        await self.db.commit()
        await self.db.refresh(game)
        return game

    async def advance_round(self, game: Game) -> tuple[Game, int]:
        income = round_salary_income(game.age_round, game.employment_status)
        game.money += income
        game.age_round += 1
        game.age_range = AGE_RANGES[game.age_round]
        await self.db.commit()
        await self.db.refresh(game)
        return game, income

    async def apply_final_round_salary(self, game: Game) -> int:
        """第 8 轮结束后结算最后一轮工资（无 advance-round）。"""
        income = round_salary_income(game.age_round, game.employment_status)
        game.money += income
        await self.db.commit()
        await self.db.refresh(game)
        return income

    async def complete_game(self, game: Game, *, ai_review: str) -> Game:
        game.status = "completed"
        game.ai_review = ai_review
        await self.db.commit()
        await self.db.refresh(game)
        return game
