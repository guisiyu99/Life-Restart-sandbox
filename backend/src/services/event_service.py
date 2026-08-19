"""事件抽取：AI 生成 + 预设降级。"""

from __future__ import annotations

import json
import random
import uuid
from pathlib import Path
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from pycore.core import get_logger
from src.api.exceptions import APIError
from src.constants.game import (
    can_pick_circle_only,
    can_pick_theme,
    get_events_per_round,
    is_fully_random,
    pick_random_circle,
    pick_random_theme,
    themes_for_circle,
)
from src.db.models import Game
from src.models.game import DrawEventRequest, DrawEventResponse, EventOptionPublic, GameEventPublic
from src.repositories.game_repo import GameRepository
from src.services.ai_service import AIService

logger = get_logger()

_PRESET_PATH = Path(__file__).resolve().parents[1] / "data" / "preset_events.json"
_PRESET_CACHE: dict[str, list[dict[str, Any]]] | None = None


def _load_presets() -> dict[str, list[dict[str, Any]]]:
    global _PRESET_CACHE
    if _PRESET_CACHE is None:
        with _PRESET_PATH.open(encoding="utf-8") as file:
            _PRESET_CACHE = json.load(file)
    return _PRESET_CACHE


def _new_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:10]}"


def _normalize_event(raw: dict[str, Any]) -> GameEventPublic:
    title = str(raw.get("title", "")).strip()
    description = str(raw.get("description", "")).strip()
    if not title or not description:
        raise ValueError("Event missing title or description")

    options_raw = raw.get("options") or []
    if not isinstance(options_raw, list) or not (2 <= len(options_raw) <= 3):
        raise ValueError("Event must have 2-3 options")

    options: list[EventOptionPublic] = []
    for opt in options_raw:
        if not isinstance(opt, dict):
            raise ValueError("Invalid option")
        text = str(opt.get("text", "")).strip()
        if not text:
            raise ValueError("Option missing text")
        options.append(
            EventOptionPublic(
                option_id=str(opt.get("option_id") or _new_id("opt")),
                text=text,
                money_change=int(opt.get("money_change", 0)),
                energy_change=int(opt.get("energy_change", 0)),
                joy_change=int(opt.get("joy_change", 0)),
            )
        )

    return GameEventPublic(
        event_id=str(raw.get("event_id") or _new_id("evt")),
        title=title,
        description=description,
        options=options,
    )


class EventService:
    def __init__(self, db: AsyncSession) -> None:
        self.game_repo = GameRepository(db)
        self.ai = AIService()

    def _resolve_circle_theme(
        self, game: Game, body: DrawEventRequest
    ) -> tuple[str, str]:
        age_round = game.age_round

        if can_pick_theme(age_round):
            if body.circle not in ("life", "career"):
                raise APIError(code=4000, message="请选择生活圈或事业圈", status_code=400)
            if not body.theme:
                raise APIError(code=4000, message="请选择子主题", status_code=400)
            allowed = themes_for_circle(body.circle)
            if body.theme not in allowed:
                raise APIError(code=4000, message="无效的子主题", status_code=400)
            return body.circle, body.theme

        if can_pick_circle_only(age_round):
            if body.circle not in ("life", "career"):
                raise APIError(code=4000, message="请选择生活圈或事业圈", status_code=400)
            return body.circle, pick_random_theme(body.circle)

        if is_fully_random(age_round):
            circle = pick_random_circle()
            return circle, pick_random_theme(circle)

        raise APIError(code=4000, message="无效的游戏阶段", status_code=400)

    def _pick_preset(self, theme: str) -> GameEventPublic:
        presets = _load_presets()
        pool = presets.get(theme) or presets.get("default", [])
        if not pool:
            raise RuntimeError("Preset events missing")
        raw = random.choice(pool)
        return _normalize_event(raw)

    async def _generate_event(
        self,
        game: Game,
        circle: str,
        theme: str,
    ) -> GameEventPublic:
        try:
            raw = await self.ai.generate_event(
                age_range=game.age_range,
                age_round=game.age_round,
                circle=circle,
                theme=theme,
                money=game.money,
                energy=game.energy,
                joy=game.joy,
            )
            return _normalize_event(raw)
        except Exception as exc:
            logger.warning(
                "AI event generation failed, using preset fallback",
                error_msg=str(exc),
                theme=theme,
            )
            return self._pick_preset(theme)

    async def draw_event(
        self,
        game_id: int,
        user_id: int,
        body: DrawEventRequest,
    ) -> DrawEventResponse:
        game = await self.game_repo.get_by_id_for_user(game_id, user_id)
        if game is None:
            raise APIError(code=4004, message="游戏不存在", status_code=404)
        if game.status == "completed":
            raise APIError(code=4005, message="游戏已完成，无法继续", status_code=400)

        circle, theme = self._resolve_circle_theme(game, body)
        event = await self._generate_event(game, circle, theme)
        count = get_events_per_round(game.age_round)
        return DrawEventResponse(events=[event], count=count)
