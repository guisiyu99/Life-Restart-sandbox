"""draw-event 接口测试。"""

from __future__ import annotations

from typing import cast
from unittest.mock import AsyncMock, patch

import pytest
from httpx import AsyncClient


async def _create_game(client: AsyncClient, headers: dict[str, str]) -> int:
    response = await client.post("/api/games", headers=headers, json={})
    return cast(int, response.json()["data"]["id"])


@pytest.mark.asyncio
async def test_draw_event_fallback_preset(client: AsyncClient, auth_headers: dict[str, str]) -> None:
    game_id = await _create_game(client, auth_headers)

    with patch(
        "src.services.event_service.AIService.generate_event",
        new_callable=AsyncMock,
        side_effect=RuntimeError("AI unavailable"),
    ):
        response = await client.post(
            f"/api/games/{game_id}/draw-event",
            headers=auth_headers,
            json={"circle": "life", "theme": "友情"},
        )

    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 200
    events = data["data"]["events"]
    assert len(events) == 1
    assert events[0]["title"]
    assert 2 <= len(events[0]["options"]) <= 3
    assert data["data"]["count"] == 2


@pytest.mark.asyncio
async def test_draw_event_requires_circle_and_theme(client: AsyncClient, auth_headers: dict[str, str]) -> None:
    game_id = await _create_game(client, auth_headers)
    response = await client.post(
        f"/api/games/{game_id}/draw-event",
        headers=auth_headers,
        json={"circle": "life"},
    )
    assert response.status_code == 400
    assert response.json()["code"] == 4000


@pytest.mark.asyncio
async def test_draw_event_game_not_found(client: AsyncClient, auth_headers: dict[str, str]) -> None:
    response = await client.post(
        "/api/games/99999/draw-event",
        headers=auth_headers,
        json={"circle": "life", "theme": "父母"},
    )
    assert response.status_code == 404
    assert response.json()["code"] == 4004


@pytest.mark.asyncio
async def test_draw_event_with_mock_ai(client: AsyncClient, auth_headers: dict[str, str]) -> None:
    game_id = await _create_game(client, auth_headers)
    mock_event = {
        "title": "AI 生成测试事件",
        "description": "这是一段由 AI 生成的测试描述，用于验证解析逻辑。",
        "options": [
            {"text": "选项 A", "money_change": 1000, "energy_change": 0, "joy_change": 1},
            {"text": "选项 B", "money_change": -500, "energy_change": 1, "joy_change": 0},
        ],
    }

    with patch(
        "src.services.event_service.AIService.generate_event",
        new_callable=AsyncMock,
        return_value=mock_event,
    ):
        response = await client.post(
            f"/api/games/{game_id}/draw-event",
            headers=auth_headers,
            json={"circle": "career", "theme": "工作"},
        )

    assert response.status_code == 200
    event = response.json()["data"]["events"][0]
    assert event["title"] == "AI 生成测试事件"
    assert event["event_id"].startswith("evt_")
