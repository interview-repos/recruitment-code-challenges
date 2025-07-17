from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = ""
    secret_key: str = ""
    algorithm: str = ""
    access_token_expiry: int = 60

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
