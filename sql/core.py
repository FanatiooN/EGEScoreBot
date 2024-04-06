import pandas as pd
from loguru import logger
from sqlalchemy import delete, insert, select

from config import settings
from sql.database import engine
from sql.models import metadata, student_subject, students, subjects
from typing import Dict, List, Union


def create_tables() -> None:
    try:
        metadata.create_all(engine)
        logger.info("create tables")

        if len(get_subjects()) == 0:
            for subject_id, subject_name in settings.CLASS_TYPES.items():
                insert_subject(subject_id, subject_name)

    except Exception as e:
        logger.error(f"{e}")


def insert_student(telegram_id: int, name: str, surname: str) -> None:
    try:
        with engine.connect() as conn:
            statement = insert(students).values(
                [
                    {
                        "telegram_id": telegram_id,
                        "student_name": name,
                        "student_surname": surname,
                    },
                ]
            )
            conn.execute(statement)
            conn.commit()
            logger.info(f"insert student {name} {surname}")

    except Exception as e:
        logger.error(f"{e}")


def insert_subject(subject_id: int, subject_name: str) -> None:
    try:
        with engine.connect() as conn:
            statement = insert(subjects).values(
                [
                    {"subject_id": f"{subject_id}", "subject_name": subject_name},
                ]
            )
            conn.execute(statement)
            conn.commit()
            logger.info(f"insert subject {subject_name}")

    except Exception as e:
        logger.error(f"{e}")


def insert_scores(student_id: int, scores: list[tuple[int, int]]) -> None:
    try:
        with engine.connect() as conn:
            statement = insert(student_subject).values(
                [
                    {
                        "student_id": student_id,
                        "subject_id": subject_id,
                        "score": score,
                    }
                    for subject_id, score in scores
                ]
            )
            conn.execute(statement)
            conn.commit()
            logger.info(f"insert scores {student_id} {subject_id} {scores}")

    except Exception as e:
        logger.error(f"{e}")


def get_student_id(telegram_id: int) -> None:
    try:
        with engine.connect() as conn:
            query = select(students.c.student_id).where(
                students.c.telegram_id == telegram_id
            )

            result = conn.execute(query)

            student_id = result.scalar()

            logger.info(f"get student id {telegram_id} {student_id}")
            return student_id

    except Exception as e:
        logger.error(f"{e}")


def get_scores(student_id: int) -> list[int, int, int]:
    try:
        with engine.connect() as conn:
            query = select(student_subject).where(
                student_subject.c.student_id == student_id
            )
            result = conn.execute(query)
            scores = result.fetchall()
            logger.info(f"get scores {student_id} {scores}")
            return scores

    except Exception as e:
        logger.error(f"{e}")


def get_all_students() -> List[Dict[str, Union[int, str]]]:
    with engine.connect() as conn:
        query = select(students)
        result = conn.execute(query)
        students_data = result.fetchall()
        students_list = [
            {
                "student_id": row.student_id,
                "telegram_id": row.telegram_id,
                "student_name": row.student_name,
                "student_surname": row.student_surname,
            }
            for row in students_data
        ]
        logger.info(f"get all students {students_list}")
        return students_list


def get_subjects() -> list[int, str]:
    try:
        with engine.connect() as conn:
            query = select(subjects)
            result = conn.execute(query).fetchall()
            logger.info(f"get subjects {result}")
            return result

    except Exception as e:
        logger.error(f"{e}")


def get_all_scores():
    try:
        with engine.connect() as conn:
            query = select(students, student_subject, subjects).select_from(
                students.join(
                    student_subject,
                    students.c.student_id == student_subject.c.student_id,
                ).join(subjects, student_subject.c.subject_id == subjects.c.subject_id)
            )
            result = conn.execute(query)
            scores_data = result.fetchall()

            logger.info(f"{scores_data}")
            return scores_data
    except Exception as e:
        logger.error(f"{e}")


def delete_student(student_id: int) -> None:
    try:
        with engine.connect() as conn:
            delete_scores(student_id)
            query = delete(students).where(students.c.student_id == student_id)
            logger.info(f"delete student {student_id}")
            conn.execute(query)
            conn.commit()

    except Exception as e:
        logger.error(f"{e}")


def delete_scores(student_id: int) -> None:
    try:
        with engine.connect() as conn:
            query = delete(student_subject).where(
                student_subject.c.student_id == student_id
            )
            logger.info(f"delete scores {student_id}")
            conn.execute(query)
            conn.commit()

    except Exception as e:
        logger.error(f"{e}")


def export_to_csv(filename: str = "scores.csv") -> None:
    scores_data = get_all_scores()
    logger.info(f"scores_data {scores_data}")

    df = pd.DataFrame(scores_data)
    df = df.drop(df.columns[[4, 5, 7]], axis=1)
    df.to_csv(filename, index=False, encoding="utf-8-sig")
    print(f"Данные успешно экспортированы в файл {filename}")
