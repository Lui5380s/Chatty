from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    project_name: str = "Chatty"
    database_url: str
    debug: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",   # lädt automatisch Variablen aus deiner .env
        extra="ignore"     # erlaubt zusätzliche Variablen wie APP_NAME, APP_ENV
    )

settings = Settings()