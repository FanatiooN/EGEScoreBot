from enum import Enum


class States(Enum):
    REGISTER_NAME = 1
    REGISTER_SURNAME = 2
    ENTER_SUBJECT_COUNT = 3
    SELECT_SUBJECT = 4
    ENTER_SCORES = 5


