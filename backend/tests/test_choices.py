"""choices 与 advance-round 接口测试。"""

from __future__ import annotations

from typing import cast

import pytest
from httpx import AsyncClient

CHOICE_PAYLOAD = {
    "event_id": "evt_test",
    "option_id": "opt_test",
    "circle": "life",
    "theme": "友情",
    "event_title": "老友重逢",
    "event_description": "多年未见的老友突然联系你。",
    "chosen_option_text": "约出来叙旧",
    "money_change": -2000,
    "energy_change": 2,
    "joy_change": 3,
}


async def _create_game(client: AsyncClient, headers: dict[str, str]) -> int:
    response = await client.post("/api/games", headers=headers, json={})
    return cast(int, response.json()["data"]["id"])


@pytest.mark.asyncio
async def test_submit_choice_updates_stats(client: AsyncClient, auth_headers: dict[str, str]) -> None:
    game_id = await _create_game(client, auth_headers)

    response = await client.post(
        f"/api/games/{game_id}/choices",
        headers=auth_headers,
        json=CHOICE_PAYLOAD,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 200
    game = data["data"]
    assert game["money"] == 48000
    assert game["energy"] == 12
    assert game["joy"] == 3
    assert len(game["decisions"]) == 1
    assert game["last_decision"]["chosen_option"] == "约出来叙旧"
    assert game["last_decision"]["round"] == 1


@pytest.mark.asyncio
async def test_advance_round(client: AsyncClient, auth_headers: dict[str, str]) -> None:
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
    assert response.status_code == 200
    game = response.json()["data"]
    assert game["age_round"] == 2
    assert game["age_range"] == "25-30"
    assert game["status"] == "in_progress"


@pytest.mark.asyncio
async def test_choice_persisted_on_get(client: AsyncClient, auth_headers: dict[str, str]) -> None:
    game_id = await _create_game(client, auth_headers)
    await client.post(
        f"/api/games/{game_id}/choices",
        headers=auth_headers,
        json=CHOICE_PAYLOAD,
    )

    get_res = await client.get(f"/api/games/{game_id}", headers=auth_headers)
    game = get_res.json()["data"]
    assert len(game["decisions"]) == 1
    assert game["money"] == 48000


@pytest.mark.asyncio
async def test_advance_round_at_last_round_fails(client: AsyncClient, auth_headers: dict[str, str]) -> None:
    game_id = await _create_game(client, auth_headers)

    for round_num in range(1, 9):
        for _ in range(2 if round_num < 8 else 1):
            await client.post(
                f"/api/games/{game_id}/choices",
                headers=auth_headers,
                json=CHOICE_PAYLOAD,
            )
        if round_num < 8:
            await client.post(
                f"/api/games/{game_id}/advance-round",
                headers=auth_headers,
            )

    response = await client.post(
        f"/api/games/{game_id}/advance-round",
        headers=auth_headers,
    )
    assert response.status_code == 400
    assert response.json()["code"] == 4005


@pytest.mark.asyncio
async def test_choice_requires_auth(client: AsyncClient) -> None:
    response = await client.post("/api/games/1/choices", json=CHOICE_PAYLOAD)
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_choice_game_not_found(client: AsyncClient, auth_headers: dict[str, str]) -> None:
    response = await client.post(
        "/api/games/99999/choices",
        headers=auth_headers,
        json=CHOICE_PAYLOAD,
    )
    assert response.status_code == 404
    assert response.json()["code"] == 4004
