from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import registry

metadata = MetaData()
mapper_registry = registry()

students = Table(
    "students",
    metadata,
    Column("student_id", Integer, primary_key=True, autoincrement=True),
    Column("telegram_id", Integer, primary_key=True),
    Column("student_name", String(255), nullable=False),
    UniqueConstraint("student_id", name="uix_student_id"),
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
    Column("student_id", Integer, ForeignKey("students.student_id")),
    Column("subject_id", Integer, ForeignKey("subjects.subject_id")),
    Column("score", Integer),
)
