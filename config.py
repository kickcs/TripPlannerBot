from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr
from typing import List, Optional


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    BOT_TOKEN: SecretStr
    ADMIN_IDS: str

    def get_admin_ids_list(self) -> List[int]:
        return [int(admin_id) for admin_id in self.ADMIN_IDS.split(",") if admin_id.strip().isdigit()]

    @property
    def DATABASE_URL(self):
        # postgresql+asyncpg://postgres:postgres@localhost:5432/sa
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
