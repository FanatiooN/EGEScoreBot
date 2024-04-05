from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Dict
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


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

    WELCOME_MSG: str = (
            "Привет! Я бот для сбора баллов ЕГЭ. "
            "Вы можете использовать следующие команды:\n\n"
            "/register - Зарегистрироваться в системе\n"
            "/enter_scores - Внести баллы ЕГЭ\n"
            "/view_scores - Просмотреть свои баллы ЕГЭ\n"
        )

    @property
    def classes_markup(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text=value, callback_data=str(key))
                    for key, value in list(self.CLASS_TYPES.items())[i: i + 3]
                ]
                for i in range(0, len(self.CLASS_TYPES), 3)
            ]
        )

    @property
    def database_url(self):
        return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?client_encoding=utf8'"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
