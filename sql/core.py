from sql.database import engine
from sql.models import metadata, students, subjects, student_subject
from sqlalchemy import insert, select, delete


def create_tables():
    metadata.drop_all(engine, checkfirst=True)
    metadata.create_all(engine)


def insert_student(telegram_id: int, name: str):
    with engine.connect() as conn:
        statement = insert(students).values(
            [
                {"telegram_id": telegram_id, "student_name": name},
            ]
        )
        conn.execute(statement)
        conn.commit()


def insert_subject(subject_id: int, subject_name: str):
    with engine.connect() as conn:
        statement = insert(subjects).values(
            [
                {"subject_id": f"{subject_id}", "subject_name": subject_name},
            ]
        )
        conn.execute(statement)
        conn.commit()


def insert_scores(student_id: int, scores: list[tuple[int, int]]):
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


def get_student_id(telegram_id: int):
    with engine.connect() as conn:
        query = select(students.c.student_id).where(
            students.c.telegram_id == telegram_id
        )

        result = conn.execute(query)

        student_id = result.scalar()

        return student_id


def get_scores(student_id: int):
    with engine.connect() as conn:
        query = select(student_subject).where(
            student_subject.c.student_id == student_id
        )

        result = conn.execute(query)

        scores = result.fetchall()

        return scores


def delete_student(student_id: int):
    with engine.connect() as conn:
        query = delete(students).where(students.c.student_id == student_id)

        conn.execute(query)


def delete_scores(student_id: int):
    with engine.connect() as conn:
        query = delete(student_subject).where(
            student_subject.c.student_id == student_id
        )

        conn.execute(query)
