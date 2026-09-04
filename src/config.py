"""Application environment and runtime configuration."""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent


class BaseConfig:
    APP_NAME: str = "Nilgiri Dairy Pro"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    TESTING: bool = False
    SECRET_KEY: str = os.getenv("SECRET_KEY", "default-dev-secret-key-change-in-prod")
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", f"sqlite+aiosqlite:///{BASE_DIR}/dairy.db"
    )
    BACKUP_DIR: str = os.getenv("BACKUP_DIR", str(BASE_DIR / "backups"))


class DevelopmentConfig(BaseConfig):
    DEBUG: bool = True


class TestingConfig(BaseConfig):
    DEBUG: bool = True
    TESTING: bool = True
    DATABASE_URL: str = "sqlite+aiosqlite:///:memory:"


class ProductionConfig(BaseConfig):
    DEBUG: bool = False


# Aliases expected by tests & database connection
Config = DevelopmentConfig

config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}

config = config_by_name.get(os.getenv("ENV", "development"), DevelopmentConfig)
