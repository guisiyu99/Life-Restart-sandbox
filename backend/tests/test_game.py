"""游戏创建与查询测试。"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_and_get_game(client: AsyncClient, auth_headers: dict[str, str]) -> None:
    create_res = await client.post(
        "/api/games",
        headers=auth_headers,
        json={"money": 55000, "energy": 12, "joy": 1},
    )
    assert create_res.status_code == 200
    create_data = create_res.json()
    assert create_data["code"] == 200
    game = create_data["data"]
    assert game["money"] == 55000
    assert game["energy"] == 12
    assert game["joy"] == 1
    assert game["age_round"] == 1
    assert game["age_range"] == "22-25"
    assert game["decisions"] == []
    assert game["status"] == "in_progress"

    game_id = game["id"]
    get_res = await client.get(f"/api/games/{game_id}", headers=auth_headers)
    assert get_res.status_code == 200
    assert get_res.json()["data"]["id"] == game_id


@pytest.mark.asyncio
async def test_create_game_default_stats(client: AsyncClient, auth_headers: dict[str, str]) -> None:
    response = await client.post("/api/games", headers=auth_headers, json={})
    assert response.status_code == 200
    game = response.json()["data"]
    assert game["money"] == 50000
    assert game["energy"] == 10
    assert game["joy"] == 0


@pytest.mark.asyncio
async def test_get_game_not_found(client: AsyncClient, auth_headers: dict[str, str]) -> None:
    response = await client.get("/api/games/99999", headers=auth_headers)
    assert response.status_code == 404
    assert response.json()["code"] == 4004


@pytest.mark.asyncio
async def test_get_game_requires_auth(client: AsyncClient) -> None:
    response = await client.get("/api/games/1")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_create_game_requires_auth(client: AsyncClient) -> None:
    response = await client.post("/api/games", json={})
    assert response.status_code == 401
