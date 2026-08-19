"""认证接口测试。"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_and_login_flow(client: AsyncClient) -> None:
    register_res = await client.post(
        "/api/auth/register",
        json={"email": "newuser@example.com", "password": "password123"},
    )
    assert register_res.status_code == 200
    register_data = register_res.json()
    assert register_data["code"] == 200
    assert register_data["data"]["access_token"]
    assert register_data["data"]["user"]["email"] == "newuser@example.com"

    login_res = await client.post(
        "/api/auth/login",
        json={"email": "newuser@example.com", "password": "password123"},
    )
    assert login_res.status_code == 200
    token = login_res.json()["data"]["access_token"]

    me_res = await client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert me_res.status_code == 200
    assert me_res.json()["data"]["email"] == "newuser@example.com"


@pytest.mark.asyncio
async def test_register_duplicate_returns_4003(client: AsyncClient) -> None:
    payload = {"email": "dup@example.com", "password": "password123"}
    first = await client.post("/api/auth/register", json=payload)
    assert first.status_code == 200

    second = await client.post("/api/auth/register", json=payload)
    assert second.status_code == 400
    data = second.json()
    assert data["code"] == 4003
    assert data["message"] == "用户已存在"


@pytest.mark.asyncio
async def test_login_wrong_password_returns_4001(client: AsyncClient) -> None:
    await client.post(
        "/api/auth/register",
        json={"email": "loginuser@example.com", "password": "password123"},
    )
    res = await client.post(
        "/api/auth/login",
        json={"email": "loginuser@example.com", "password": "wrongpass"},
    )
    assert res.status_code == 401
    data = res.json()
    assert data["code"] == 4001
    assert data["message"] == "用户名或密码错误"
