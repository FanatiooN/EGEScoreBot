import re

from plugins.FSM import States
from config import settings
from loguru import logger
from pyrogram.types import Message, CallbackQuery
from pyrogram import Client, filters
from sql.core import (
    delete_student,
    insert_student,
    get_student_id,
    get_scores,
    delete_scores,
    insert_scores,
    export_to_csv,
)

user_states = {}
register_temp = {}
scores_temp = {}


def check_text(text: str):
    return re.match(r"^[а-яА-ЯёЁa-zA-Z\-\s]+$", text) is not None


@Client.on_message(filters.command("register") & filters.private)
async def register(client: Client, message: Message) -> None:
    try:
        user_id = message.from_user.id
        student_id = get_student_id(user_id)
        if student_id is not None:
            delete_student(student_id)

        register_temp[user_id] = {"name": None, "surname": None}
        user_states[user_id] = States.REGISTER_NAME

        await message.reply("Введите имя")
    except Exception as e:
        logger.error(f"{e}")


@Client.on_message(filters.command("start") & filters.private)
async def start(client: Client, message: Message) -> None:
    try:
        await message.reply(settings.WELCOME_MSG)
    except Exception as e:
        logger.error(f"{e}")


@Client.on_message(filters.command("view_scores") & filters.private)
async def view_scores(client: Client, message: Message) -> None:
    try:
        user_id = message.from_user.id
        student_id = get_student_id(user_id)

        if student_id is None:
            await message.reply(
                "Перед вводом баллов необходимо зарегистрироваться.\n"
                "Пожалуйста, используйте команду /register"
            )
        else:
            if student_id is not None:
                scores = get_scores(student_id)
                if scores:
                    scores_message = "Ваши баллы ЕГЭ:\n"
                    for student_id, subject_name, score in scores:
                        scores_message += (
                            f"{settings.CLASS_TYPES[subject_name]} — {score}\n"
                        )
                    await message.reply(scores_message)
                else:
                    await message.reply("У вас нет сохраненных баллов ЕГЭ.")
            else:
                await message.reply("Вы не зарегистрированы в системе.")
    except Exception as e:
        logger.error(f"{e}")


@Client.on_message(filters.command("enter_scores") & filters.private)
async def enter_scores(client: Client, message: Message) -> None:
    try:
        user_id = message.from_user.id
        student_id = get_student_id(user_id)

        if student_id is None:
            await message.reply(
                "Перед вводом баллов необходимо зарегистрироваться.\n"
                "Пожалуйста, используйте команду /register"
            )

        else:
            scores = get_scores(student_id)
            if scores:
                delete_scores(student_id)
                await message.reply("Предыдущие результаты были успешно удалены")

            user_states[user_id] = States.ENTER_SUBJECT_COUNT
            await message.reply("Введите кол-во предметов, которые вы сдавали")

    except Exception as e:
        logger.error(f"{e}")


@Client.on_message(filters.command("export") & filters.private)
async def export_data(client: Client, message: Message) -> None:
    try:
        logger.info("start")
        export_to_csv()

        await message.reply_document("scores.csv")

    except Exception as e:
        await message.reply(f"{e}")


@Client.on_message(filters.private)
async def handle(client: Client, message: Message) -> None:
    try:
        user_id = message.from_user.id

        if user_id in user_states:
            if user_states[user_id] == States.REGISTER_NAME:
                if message.text is not None and check_text(message.text):

                    register_temp[user_id]["name"] = message.text
                    user_states[user_id] = States.REGISTER_SURNAME
                    await message.reply("Введите фамилию")
                else:
                    await message.reply("Введите имя, состоящее только из букв!")

            elif user_states[user_id] == States.REGISTER_SURNAME:
                if message.text is not None and check_text(message.text):
                    register_temp[user_id]["surname"] = message.text

                    name = register_temp[user_id]["name"]
                    surname = register_temp[user_id]["surname"]
                    insert_student(user_id, name, surname)

                    del user_states[user_id]
                    del register_temp[user_id]
                    await message.reply("Регистрация завершена!")
                else:
                    await message.reply("Введите фамилию, состоящую только из букв!")

            elif user_states[user_id] == States.ENTER_SUBJECT_COUNT:
                data = message.text
                if data is not None and data.isdigit() and 1 <= int(data) <= 12:
                    subject_cnt = int(message.text)
                    scores_temp[user_id] = {
                        "subject_cnt": subject_cnt,
                        "last_subject_id": None,
                        "scores": [],
                    }
                    user_states[user_id] = States.SELECT_SUBJECT
                    await message.reply(
                        "Выберите предмет", reply_markup=settings.classes_markup
                    )
                else:
                    await message.reply(
                        "Пожалуйста, введите корректное кол-во предметов"
                    )

            elif user_states[user_id] == States.ENTER_SCORES:

                score = message.text

                # Необходимо отдельно обработать Базовую математику. В ней шкала от 2 до 5, на других предметах шкала - от 0 до 100
                subject_id = scores_temp[user_id]["last_subject_id"]
                if subject_id == "9":
                    min_score = 2
                    max_score = 5
                else:
                    min_score = 0
                    max_score = 100

                if (
                    score is not None
                    and score.isdigit()
                    and min_score <= int(score) <= max_score
                ):

                    last_subject_id = scores_temp[user_id]["last_subject_id"]
                    scores_temp[user_id]["last_subject_id"] = None
                    scores_temp[user_id]["scores"].append((last_subject_id, int(score)))
                    scores_temp[user_id]["subject_cnt"] -= 1

                    if scores_temp[user_id]["subject_cnt"] == 0:
                        student_id = get_student_id(user_id)
                        insert_scores(student_id, scores_temp[user_id]["scores"])
                        await message.reply("Баллы успешно внесены!")
                    else:
                        user_states[user_id] = States.SELECT_SUBJECT
                        await message.reply(
                            "Выберите предмет", reply_markup=settings.classes_markup
                        )
                else:
                    await message.reply(
                        f"Неверно введён балл. Пожалуйста, введите балл от {min_score} до {max_score}"
                    )

    except Exception as e:
        logger.error(f"{e}")


@Client.on_callback_query()
async def enter_subject(client: Client, call: CallbackQuery) -> None:
    try:
        await client.edit_message_reply_markup(
            chat_id=call.message.chat.id, message_id=call.message.id, reply_markup=None
        )
        if call.from_user.id in user_states:
            user_id = call.from_user.id
            if user_states[user_id] == States.SELECT_SUBJECT:
                subject_id = call.data
                added_subjects = [i[0] for i in scores_temp[user_id]["scores"]]
                if subject_id in added_subjects:
                    await call.message.reply(
                        "Балл по этому предмету уже был введён. Пожалуйста, выберите другой предмет",
                        reply_markup=settings.classes_markup,
                    )
                else:
                    scores_temp[user_id]["last_subject_id"] = subject_id

                    # Необходимо отдельно обработать Базовую математику. В ней шкала от 2 до 5, на других предметах шкала - от 0 до 100
                    if subject_id == "9":
                        min_score = 2
                        max_score = 5
                    else:
                        min_score = 0
                        max_score = 100

                    user_states[user_id] = States.ENTER_SCORES
                    await call.message.reply(
                        f"Введите балл {settings.CLASS_TYPES[int(subject_id)].upper()} (от {min_score} до {max_score})\n"
                    )

    except Exception as e:
        logger.error(f"{e}")
