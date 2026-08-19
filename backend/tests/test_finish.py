"""finish 接口测试。"""

from __future__ import annotations

from typing import cast
from unittest.mock import AsyncMock, patch

import pytest
from httpx import AsyncClient

from tests.test_choices import CHOICE_PAYLOAD

async def _create_game(client: AsyncClient, headers: dict[str, str]) -> int:
    response = await client.post("/api/games", headers=headers, json={})
    return cast(int, response.json()["data"]["id"])


async def _play_to_round_8(client: AsyncClient, game_id: int, headers: dict[str, str]) -> None:
    for round_num in range(1, 9):
        events = 2 if round_num < 8 else 1
        for _ in range(events):
            await client.post(
                f"/api/games/{game_id}/choices",
                headers=headers,
                json=CHOICE_PAYLOAD,
            )
        if round_num < 8:
            await client.post(
                f"/api/games/{game_id}/advance-round",
                headers=headers,
            )


@pytest.mark.asyncio
async def test_finish_with_ai_mock(client: AsyncClient, auth_headers: dict[str, str]) -> None:
    game_id = await _create_game(client, auth_headers)
    await _play_to_round_8(client, game_id, auth_headers)

    with patch(
        "src.services.game_service.AIService.generate_life_review",
        new_callable=AsyncMock,
        return_value="你的一生充满选择与成长，最终在财富与喜悦间找到了属于自己的平衡。",
    ):
        response = await client.post(
            f"/api/games/{game_id}/finish",
            headers=auth_headers,
        )

    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 200
    result = data["data"]
    assert result["ai_review"]
    assert result["outcome_tags"]
    assert len(result["decisions"]) == 15

    get_res = await client.get(f"/api/games/{game_id}", headers=auth_headers)
    game = get_res.json()["data"]
    assert game["status"] == "completed"
    assert game["ai_review"]


@pytest.mark.asyncio
async def test_finish_ai_fallback(client: AsyncClient, auth_headers: dict[str, str]) -> None:
    game_id = await _create_game(client, auth_headers)
    await _play_to_round_8(client, game_id, auth_headers)

    with patch(
        "src.services.game_service.AIService.generate_life_review",
        new_callable=AsyncMock,
        side_effect=RuntimeError("AI unavailable"),
    ):
        response = await client.post(
            f"/api/games/{game_id}/finish",
            headers=auth_headers,
        )

    data = response.json()
    assert data["code"] == 5002
    assert "默认总结" in data["message"]
    assert data["data"]["ai_review"]
    assert len(data["data"]["decisions"]) == 15


@pytest.mark.asyncio
async def test_finish_before_round_8_fails(client: AsyncClient, auth_headers: dict[str, str]) -> None:
    game_id = await _create_game(client, auth_headers)
    response = await client.post(f"/api/games/{game_id}/finish", headers=auth_headers)
    assert response.status_code == 400
    assert response.json()["code"] == 4000


@pytest.mark.asyncio
async def test_finish_requires_auth(client: AsyncClient) -> None:
    response = await client.post("/api/games/1/finish")
    assert response.status_code == 401
