from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    DB_URL: str = "sqlite+aiosqlite:///./answer_requester_db.db"

    class Config:
        case_sensitive = False
        env_file = ".env"

settings = Settings()