"""
重启人生沙盘模拟 — 后端应用入口。

运行: cd backend && PYTHONPATH=.. python3 -m uvicorn src.main:app --host 127.0.0.1 --port 8099
"""

from __future__ import annotations

from fastapi import Request
from fastapi.responses import JSONResponse

from pycore.api import APIConfig, APIServer
from pycore.core import Logger, LoggerConfig, LogLevel, get_logger
from src.api.exceptions import APIError
from src.api.routes.archive import router as archive_router
from src.api.routes.auth import router as auth_router
from src.api.routes.game import router as game_router
from src.core.config import settings
from src.db.session import close_db, init_db

Logger.configure(
    LoggerConfig(
        level=LogLevel.DEBUG if settings.debug else LogLevel.INFO,
        app_name="life-restart-sandbox",
        json_format=False,
    )
)
logger = get_logger()

server = APIServer(
    APIConfig(
        title="重启人生沙盘模拟 API",
        version="1.0.0",
        host=settings.host,
        port=settings.port,
        debug=settings.debug,
        cors_origins=settings.cors_origins,
    )
)


@server.on_startup
async def startup() -> None:
    """应用启动。"""
    await init_db()
    logger.info("Application starting", host=settings.host, port=settings.port)


@server.on_shutdown
async def shutdown() -> None:
    """应用关闭。"""
    await close_db()
    logger.info("Application shutting down")


server.include_router(auth_router)
server.include_router(game_router)
server.include_router(archive_router)

app = server.app


@app.exception_handler(APIError)
async def api_error_handler(_request: Request, exc: APIError) -> JSONResponse:
    """统一契约错误响应。"""
    return JSONResponse(
        status_code=exc.status_code,
        content={"code": exc.code, "message": exc.message, "data": None},
    )
