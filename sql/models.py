from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.orm import registry

metadata = MetaData()
mapper_registry = registry()

students = Table(
    "students",
    metadata,
    Column("telegram_id", Integer, primary_key=True),
    Column("student_name", String(255), nullable=False),
)

subjects = Table(
    "subjects",
    metadata,
    Column("subject_id", Integer, primary_key=True),
    Column("subject_name", String(255), nullable=False),
)

student_subject = Table(
    "student_subject",
    metadata,
    Column(
        "telegram_id", Integer, ForeignKey("students.telegram_id"), primary_key=True
    ),
    Column("subject_id", Integer, ForeignKey("subjects.subject_id"), primary_key=True),
    Column("score", Integer),
)
