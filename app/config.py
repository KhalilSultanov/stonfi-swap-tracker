from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    STONFI_CONTRACT_MAINNET: str
    TONAPI_BASE_URL: str
    TONAPI_KEY: str
    STONFI_CONTRACT_MAINNET: str
    STONFI_CONTRACT_TESTNET: str

    @property
    def SQLALCHEMY_DATABASE_URL(self) -> str:
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    class Config:
        env_file = Path(__file__).resolve().parent.parent / ".env"


settings = Settings()
