"""archives 接口测试。"""

from __future__ import annotations

from typing import cast
from unittest.mock import AsyncMock, patch

import pytest
from httpx import AsyncClient

from tests.test_choices import CHOICE_PAYLOAD


async def _create_and_finish(client: AsyncClient, headers: dict[str, str]) -> int:
    game_id = cast(
        int,
        (await client.post("/api/games", headers=headers, json={})).json()["data"]["id"],
    )
    for round_num in range(1, 9):
        events = 2 if round_num < 8 else 1
        for _ in range(events):
            await client.post(
                f"/api/games/{game_id}/choices",
                headers=headers,
                json=CHOICE_PAYLOAD,
            )
        if round_num < 8:
            await client.post(f"/api/games/{game_id}/advance-round", headers=headers)

    with patch(
        "src.services.game_service.AIService.generate_life_review",
        new_callable=AsyncMock,
        return_value="归档测试用人生总结。",
    ):
        await client.post(f"/api/games/{game_id}/finish", headers=headers)
    return game_id


@pytest.mark.asyncio
async def test_list_archives_only_completed(client: AsyncClient, auth_headers: dict[str, str]) -> None:
    in_progress_id = cast(
        int,
        (await client.post("/api/games", headers=auth_headers, json={})).json()["data"]["id"],
    )
    finished_id = await _create_and_finish(client, auth_headers)

    response = await client.get("/api/archives", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()["data"]
    ids = [item["id"] for item in data["items"]]
    assert finished_id in ids
    assert in_progress_id not in ids
    assert data["total"] >= 1
    item = next(i for i in data["items"] if i["id"] == finished_id)
    assert item["status"] == "completed"
    assert item["decision_count"] == 15
    assert item["outcome_tags"]


@pytest.mark.asyncio
async def test_get_archive_detail(client: AsyncClient, auth_headers: dict[str, str]) -> None:
    game_id = await _create_and_finish(client, auth_headers)
    response = await client.get(f"/api/archives/{game_id}", headers=auth_headers)
    assert response.status_code == 200
    detail = response.json()["data"]
    assert detail["id"] == game_id
    assert detail["ai_review"]
    assert len(detail["decisions"]) == 15
    assert detail["outcome_tags"]


@pytest.mark.asyncio
async def test_get_archive_not_found(client: AsyncClient, auth_headers: dict[str, str]) -> None:
    response = await client.get("/api/archives/99999", headers=auth_headers)
    assert response.status_code == 404
    assert response.json()["code"] == 4004


@pytest.mark.asyncio
async def test_in_progress_game_not_in_archive_detail(
    client: AsyncClient, auth_headers: dict[str, str]
) -> None:
    game_id = cast(
        int,
        (await client.post("/api/games", headers=auth_headers, json={})).json()["data"]["id"],
    )
    response = await client.get(f"/api/archives/{game_id}", headers=auth_headers)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_archives_requires_auth(client: AsyncClient) -> None:
    response = await client.get("/api/archives")
    assert response.status_code == 401
