from pathlib import Path
from dataclasses import dataclass
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent

class DB_settings(BaseModel):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    @property
    def DATABASE_URL_asyncpg(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def DATABASE_URL_psycopg(self) -> str:
        return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

class AuthJWT(BaseModel):
    private_key_path:Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path:Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm:str = "RS256"
    access_token_expire_minutes:int = 2
    refresh_token_expire_days:int = 7

class Settings(BaseSettings):
    db_settings:DB_settings
    jwt_settings:AuthJWT = AuthJWT()

    model_config = SettingsConfigDict(
        env_file=".env",
        env_nested_delimiter="__"
    )

settings = Settings()