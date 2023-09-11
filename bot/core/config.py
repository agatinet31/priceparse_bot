import os
from pathlib import Path
from typing import Optional

from pydantic import SecretStr

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent


class Settings(BaseSettings):
    """Класс конфигурации сервиса."""

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8"
    )
    app_title: str = "Бот парсинга цен на товары"
    description: str = "Сервис парсит информацию по ссылкам на товары"
    bot_token: SecretStr
    webhook_domain: Optional[str] = None
    webhook_path: Optional[str] = None
    app_host: Optional[str] = "0.0.0.0"
    app_port: Optional[int] = 9000
    custom_bot_api: Optional[str] = None
    datatime_format: str = "%Y-%m-%dT%H:%M:%SZ"
    sqlalchemy_database_uri: str = "sqlite+aiosqlite:///bot.db"
    import_files_root: str = os.path.join(BASE_DIR, "files")
    max_len_telegram_message: int = 4096


settings = Settings()
