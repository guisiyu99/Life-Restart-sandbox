"""
应用配置管理。

使用 pycore.core.ConfigManager + DotEnv ConfigLoader 从 backend/.env 读取配置。
禁止直接读取进程环境变量 (os.getenv / os.environ)。
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from dotenv import dotenv_values

from pycore.core import BaseSettings, ConfigLoader, ConfigManager
from pycore.core.exceptions import ConfigurationError

_ENV_KEY_ALIASES: dict[str, str] = {
    "backend_port": "port",
    "jwt_secret": "jwt_secret",
    "jwt_expire_minutes": "jwt_expire_minutes",
}


class DotEnvConfigLoader(ConfigLoader):
    """从 .env 文件加载配置，不继承进程环境变量。"""

    def supports(self, path: Path) -> bool:
        return path.suffix.lower() in (".env",) or path.name == ".env"

    def load(self, path: Path) -> dict[str, Any]:
        if not path.exists():
            raise ConfigurationError(
                f"Configuration file not found: {path}",
                config_path=str(path),
            )

        try:
            env_dict = dotenv_values(path)
            result: dict[str, Any] = {}
            for key, value in env_dict.items():
                if value is None:
                    continue
                normalized_key = key.lower()
                target_key = _ENV_KEY_ALIASES.get(normalized_key, normalized_key)

                if normalized_key == "cors_origins":
                    if value.startswith("["):
                        try:
                            result["cors_origins"] = json.loads(value)
                        except json.JSONDecodeError:
                            result["cors_origins"] = [value]
                    else:
                        result["cors_origins"] = [item.strip() for item in value.split(",") if item.strip()]
                elif value.lower() in ("true", "false"):
                    result[target_key] = value.lower() == "true"
                elif value.isdigit():
                    result[target_key] = int(value)
                else:
                    result[target_key] = value
            return result
        except Exception as exc:
            if isinstance(exc, ConfigurationError):
                raise
            raise ConfigurationError(
                f"Failed to parse .env file: {exc}",
                config_path=str(path),
            ) from exc


class AppSettings(BaseSettings):
    """应用配置。"""

    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8099
    cors_origins: list[str] = [
        "http://localhost:5199",
        "http://127.0.0.1:5199",
        "http://localhost:5175",
        "http://127.0.0.1:5175",
    ]

    database_url: str = "sqlite+aiosqlite:///./data/life_restart.db"

    jwt_secret: str
    jwt_expire_minutes: int = 10080
    jwt_algorithm: str = "HS256"

    llm_api_key: str = ""
    llm_base_url: str = "https://api.deepseek.com"
    llm_model: str = "deepseek-chat"


def _resolve_env_path() -> Path:
    candidates = [
        Path("backend/.env"),
        Path("../.env"),
        Path(".env"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    example_candidates = [
        Path("backend/.env.example"),
        Path("../.env.example"),
        Path(".env.example"),
    ]
    for example in example_candidates:
        if example.exists():
            raise ConfigurationError(
                f".env file not found. Please copy {example} to .env and configure it.",
                config_path=str(candidates[0]),
            )
    raise ConfigurationError(".env file not found and no .env.example available.")


config_manager = ConfigManager[AppSettings]()
config_manager.register_loader(DotEnvConfigLoader())
config_manager.load(AppSettings, _resolve_env_path())

settings = config_manager.settings
