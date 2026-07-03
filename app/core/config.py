from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Ponto Mais
    pm_api_token: str = ""
    pm_api_base_url: str = "https://api.pontomais.com.br/external_api/v1"

    # Supabase
    supabase_url: str = ""
    supabase_service_key: str = ""

    # Job
    job_hora: str = "06:00"

    # Notificações
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_pass: str = ""
    email_rh: str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    return Settings()
