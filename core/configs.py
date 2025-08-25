from pydantic_settings import BaseSettings
from sqlalchemy.orm import declarative_base
import os

class Settings(BaseSettings):
    API_V1_STR: str = '/api/v1'
    DB_URL: str = 'mysql+asyncmy://root:root@127.0.0.1:3306/answer_requester_db'
    DBBaseModel = declarative_base()

    class Config:
        case_sensitive = False
        env_file = os.path.join(os.path.dirname(__file__), '.env')  

settings = Settings()