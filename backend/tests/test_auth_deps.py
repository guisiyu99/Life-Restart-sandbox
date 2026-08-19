"""认证依赖与受保护路由测试。"""

import pytest
from httpx import ASGITransport, AsyncClient


@pytest.mark.asyncio
async def test_protected_route_without_token_returns_401() -> None:
    from src.main import app

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
        trust_env=False,
    ) as client:
        response = await client.get("/api/auth/me")
        assert response.status_code == 401
        data = response.json()
        assert data["code"] == 4002
        assert data["message"] == "Token 无效或过期"
        assert data["data"] is None


@pytest.mark.asyncio
async def test_protected_route_with_invalid_token_returns_401() -> None:
    from src.main import app

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
        trust_env=False,
    ) as client:
        response = await client.get(
            "/api/auth/me",
            headers={"Authorization": "Bearer invalid-token"},
        )
        assert response.status_code == 401
        data = response.json()
        assert data["code"] == 4002
        assert data["data"] is None
