import secrets

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Класс конфигурации сервиса."""

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8"
    )
    app_title: str = "Бот парсинга цен на товары"
    description: str = "Сервис парсит информацию по ссылкам на товары"
    secret: str = secrets.token_urlsafe(32)
    bot_token: str = None
    datatime_format: str = "%Y-%m-%dT%H:%M:%SZ"
    sqlalchemy_database_uri: str = "sqlite+aiosqlite:///bot.db"


settings = Settings()
