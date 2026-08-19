"""配置模块测试。"""

from src.core.config import config_manager, settings


def test_settings_load() -> None:
    assert settings.port == 8099
    assert settings.host in ("0.0.0.0", "127.0.0.1")
    assert len(settings.cors_origins) == 4
    assert "http://localhost:5199" in settings.cors_origins
    assert "http://localhost:5175" in settings.cors_origins
    assert settings.llm_model == "deepseek-chat"
    assert "sqlite" in settings.database_url


def test_config_manager_singleton() -> None:
    from pycore.core import ConfigManager

    manager1: ConfigManager = ConfigManager.instance()
    manager2: ConfigManager = ConfigManager.instance()
    assert manager1 is manager2
    assert manager1 is config_manager
