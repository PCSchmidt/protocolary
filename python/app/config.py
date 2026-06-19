"""Application configuration via pydantic-settings.

All settings are read from environment variables (or .env file).
Never import this module before the .env file is loaded.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # MongoDB
    mongo_url: str = "mongodb://localhost:27017"
    mongo_db_name: str = "transcelerate"

    # FastAPI
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    debug: bool = False

    # CDISC Library API — confirmed active 2026-04-30
    # Primary key from api.developer.library.cdisc.org
    cdisc_api_key: str = ""
    cdisc_base_url: str = "https://api.library.cdisc.org/api"
    cosmos_data_path: str = "app/data/cosmos"
    cosmos_source_commit: str = "fc11c9dbdc12aae709653b45c4c9db7f58824cf5"

    # REDCap (Gate 3+; not required for Gates 1–2)
    redcap_url: str = ""
    redcap_api_token: str = ""
    redcap_project_id: str = ""


# Module-level singleton — import this everywhere instead of constructing Settings()
settings = Settings()
