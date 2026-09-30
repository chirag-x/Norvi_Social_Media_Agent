import os
from pydantic_settings import BaseSettings, SettingsConfigDict


def _get_default_app_data_dir() -> str:
    appdata = os.getenv("APPDATA", os.path.expanduser("~"))
    return os.path.join(appdata, "Norvi", "Nexus")

class AppConfig(BaseSettings):
    """
    Application configuration validated by Pydantic.
    Loads from .env file or environment variables.
    """
    environment: str = "development"
    log_level: str = "INFO"
    app_data_dir: str = _get_default_app_data_dir()

    # Ollama
    ollama_host: str = "http://localhost:11434"
    ollama_model: str = "gemma4:cloud"

    # API Keys (Optional at startup)
    nexus_api_url: str = "https://api.nexus.local"
    nexus_api_key: str = ""
    youtube_client_id: str = ""
    youtube_client_secret: str = ""
    meta_app_id: str = ""
    meta_app_secret: str = ""

    model_config = SettingsConfigDict(
        env_file=('.env', '.env.local'),
        env_file_encoding="utf-8",
        extra="ignore",
    )

def get_config() -> AppConfig:
    return AppConfig()
