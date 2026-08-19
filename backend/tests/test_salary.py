"""轮次工资累计测试。"""

from __future__ import annotations

from typing import cast

import pytest
from httpx import AsyncClient

from src.constants.game import annual_salary_for_round, round_salary_income
from tests.test_choices import CHOICE_PAYLOAD


async def _create_game(client: AsyncClient, headers: dict[str, str]) -> int:
    response = await client.post("/api/games", headers=headers, json={})
    return cast(int, response.json()["data"]["id"])


def test_salary_constants() -> None:
    assert annual_salary_for_round(1) == 100_000
    assert annual_salary_for_round(2) == 112_000
    assert round_salary_income(1, "employed") == 300_000
    assert round_salary_income(2, "employed") == 560_000
    assert round_salary_income(1, "entrepreneur") == 0
    assert round_salary_income(1, "unemployed") == 0


@pytest.mark.asyncio
async def test_advance_round_adds_salary(client: AsyncClient, auth_headers: dict[str, str]) -> None:
    game_id = await _create_game(client, auth_headers)
    await client.post(
        f"/api/games/{game_id}/choices",
        headers=auth_headers,
        json=CHOICE_PAYLOAD,
    )

    response = await client.post(
        f"/api/games/{game_id}/advance-round",
        headers=auth_headers,
    )
    data = response.json()["data"]
    assert data["money"] == 48_000 + round_salary_income(1, "employed")
    assert data["round_salary_income"] == round_salary_income(1, "employed")
    assert data["annual_salary"] == annual_salary_for_round(2)


@pytest.mark.asyncio
async def test_finish_adds_final_round_salary(client: AsyncClient, auth_headers: dict[str, str]) -> None:
    from unittest.mock import AsyncMock, patch

    game_id = await _create_game(client, auth_headers)
    money = 50_000

    for round_num in range(1, 9):
        events = 2 if round_num < 8 else 1
        for _ in range(events):
            res = await client.post(
                f"/api/games/{game_id}/choices",
                headers=auth_headers,
                json=CHOICE_PAYLOAD,
            )
            money = res.json()["data"]["money"]
        if round_num < 8:
            adv = await client.post(
                f"/api/games/{game_id}/advance-round",
                headers=auth_headers,
            )
            money = adv.json()["data"]["money"]

    expected_before_finish = money + round_salary_income(8, "employed")

    with patch(
        "src.services.game_service.AIService.generate_life_review",
        new_callable=AsyncMock,
        return_value="总结",
    ):
        finish = await client.post(f"/api/games/{game_id}/finish", headers=auth_headers)

    assert finish.json()["data"]["money"] == expected_before_finish
