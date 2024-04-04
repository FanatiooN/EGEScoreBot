from sql.database import engine
from sql.models import metadata, students, subjects, student_subject
from sqlalchemy import insert


def create_tables():
    engine.echo = False
    metadata.drop_all(engine, checkfirst=True)
    metadata.create_all(engine)
    engine.echo = True


def insert_student(name: str):
    with engine.connect() as conn:
        statement = insert(students).values(
            [
                {"student_name": name},
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

