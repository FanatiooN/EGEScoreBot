from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Dict

class Settings(BaseSettings):
    BOT_TOKEN: str
    API_ID: str
    API_HASH: str

    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str

    CLASS_TYPES: Dict[int, str] = {
        3: "Русский язык",
        40: "Алгебра",
        1: "Математика",
        9: "Базовая математика",
        2: "Обществознание",
        7: "История",
        6: "Литература",
        10: "Английский язык",
        12: "Химия",
        4: "Биология",
        5: "Физика",
        11: "Информатика",
        25: "География",
    }

    @property
    def database_url(self):
        return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?client_encoding=utf8'"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
