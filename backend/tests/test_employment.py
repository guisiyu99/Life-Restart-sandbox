"""就业状态与工资联动测试。"""

from __future__ import annotations

from typing import cast

import pytest
from httpx import AsyncClient

from src.constants.employment import resolve_employment_status
from src.constants.game import round_salary_income
from tests.test_choices import CHOICE_PAYLOAD


def test_resolve_employment_by_theme() -> None:
    assert (
        resolve_employment_status(
            current="employed",
            theme="创业",
            event_title="朋友邀你合伙",
            event_description="...",
            chosen_option="一起创业",
        )
        == "entrepreneur"
    )


def test_resolve_unemployed_by_option() -> None:
    assert (
        resolve_employment_status(
            current="employed",
            theme="工作",
            event_title="职场压力",
            event_description="...",
            chosen_option="裸辞休息一阵",
        )
        == "unemployed"
    )


def test_resolve_reemploy() -> None:
    assert (
        resolve_employment_status(
            current="unemployed",
            theme="工作",
            event_title="新机会",
            event_description="...",
            chosen_option="接受 offer 入职",
        )
        == "employed"
    )


def test_work_theme_restores_employed_despite_event_description() -> None:
    """事件描述含「裁员/辞职」不应覆盖玩家选「工作」主题的在职判定。"""
    assert (
        resolve_employment_status(
            current="unemployed",
            theme="工作",
            event_title="部门重组",
            event_description="公司传言要裁员，你需要做出选择。",
            chosen_option="留下认真工作",
        )
        == "employed"
    )
    assert (
        resolve_employment_status(
            current="employed",
            theme="工作",
            event_title="职场压力",
            event_description="领导逼你辞职，你怎么选？",
            chosen_option="继续坚守岗位",
        )
        == "employed"
    )


def test_life_theme_does_not_false_unemploy_from_description() -> None:
    assert (
        resolve_employment_status(
            current="employed",
            theme="友情",
            event_title="朋友聚会",
            event_description="朋友说最近裁员很多，行业不景气。",
            chosen_option="安慰朋友",
        )
        == "employed"
    )


@pytest.mark.asyncio
async def test_entrepreneur_choice_skips_round_salary(client: AsyncClient, auth_headers: dict[str, str]) -> None:
    create = await client.post("/api/games", headers=auth_headers, json={})
    game_id = cast(int, create.json()["data"]["id"])

    startup_payload = {
        **CHOICE_PAYLOAD,
        "circle": "career",
        "theme": "创业",
        "event_title": "创业机会",
        "chosen_option_text": "全职创业",
    }
    await client.post(f"/api/games/{game_id}/choices", headers=auth_headers, json=startup_payload)

    adv = await client.post(f"/api/games/{game_id}/advance-round", headers=auth_headers)
    data = adv.json()["data"]
    assert data["employment_status"] == "entrepreneur"
    assert data["round_salary_income"] == 0
    assert data["money"] == 48_000


@pytest.mark.asyncio
async def test_unemployed_choice_skips_round_salary(client: AsyncClient, auth_headers: dict[str, str]) -> None:
    create = await client.post("/api/games", headers=auth_headers, json={})
    game_id = cast(int, create.json()["data"]["id"])

    quit_payload = {
        **CHOICE_PAYLOAD,
        "circle": "career",
        "theme": "工作",
        "event_title": "职场困境",
        "chosen_option_text": "辞职待业",
    }
    await client.post(f"/api/games/{game_id}/choices", headers=auth_headers, json=quit_payload)

    adv = await client.post(f"/api/games/{game_id}/advance-round", headers=auth_headers)
    data = adv.json()["data"]
    assert data["employment_status"] == "unemployed"
    assert data["round_salary_income"] == 0
    assert round_salary_income(1, "unemployed") == 0
