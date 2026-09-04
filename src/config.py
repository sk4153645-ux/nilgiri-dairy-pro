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

    # Database parameters expected by DatabaseConnection
    DATABASE_PATH: str = os.getenv("DATABASE_PATH", str(BASE_DIR / "dairy.db"))
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", f"sqlite+aiosqlite:///{BASE_DIR}/dairy.db"
    )
    DB_POOL_SIZE: int = int(os.getenv("DB_POOL_SIZE", "5"))
    DB_TIMEOUT: float = float(os.getenv("DB_TIMEOUT", "30.0"))
    BACKUP_DIR: str = os.getenv("BACKUP_DIR", str(BASE_DIR / "backups"))


class DevelopmentConfig(BaseConfig):
    DEBUG: bool = True


class TestingConfig(BaseConfig):
    DEBUG: bool = True
    TESTING: bool = True
    DATABASE_PATH: str = str(BASE_DIR / "test_dairy.db")
    DATABASE_URL: str = f"sqlite+aiosqlite:///{BASE_DIR}/test_dairy.db"
    DB_POOL_SIZE: int = 5
    DB_TIMEOUT: float = 10.0


class ProductionConfig(BaseConfig):
    DEBUG: bool = False


# Aliases
Config = DevelopmentConfig

config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}

config = config_by_name.get(os.getenv("ENV", "development"), DevelopmentConfig)
