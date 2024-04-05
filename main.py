import os
from config import settings
from loguru import logger
from pyrogram import Client, idle
import asyncio

from sql.core import (
    create_tables,
    delete_scores,
    delete_student,
    get_scores,
    get_student_id,
    insert_scores,
    insert_student,
    insert_subject,
)

logger.add(r"logs\application.log", rotation="10 MB")

plugins = dict(root="plugins")


async def main() -> None:
    # create_tables()
    my_bot_handler = Client(
        "EGEScoreBot",
        api_id=settings.API_ID,
        api_hash=settings.API_HASH,
        bot_token=settings.BOT_TOKEN,
        plugins=plugins,
        workdir="./sessions",
    )

    await my_bot_handler.start()
    await idle()
    await my_bot_handler.stop()


if __name__ == "__main__":
    asyncio.run(main())
