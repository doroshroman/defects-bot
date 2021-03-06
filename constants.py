from telegram.ext import ConversationHandler
from enum import Enum


# State constants
(
    SELECTING_ACTION,
    LOGIN_ACTION,
    REGISTER_ACTION,
    HELP_ACTION,
    SHOWING,
    ADD_DEFECT,
    DESCRIBING_DEFECT,
    CANCEL_DEFECT,
    ALL_DEFECTS,
    ALL_DEFECTS_BY_DATE,
    DEFECTS_IN_WORK,
    TAKE_DEFECT,
    CLOSE_DEFECT,
    CHANGE_DEFECT_STATUS,
) = range(14)

# user context constants
(
    START_OVER,
    SENDER_ID,
    SENDER_USERNAME,
    SENDER_FIRST_NAME,
    SENDER_LAST_NAME,
    ACCESS_TOKEN,
    ADD_DEFECT_AGAIN,
    DEFECT,
    DEFECT_TITLE,
    DEFECT_DESCRIPTION,
    DEFECT_ROOM,
    DEFECT_PHOTO,
    DEFECT_DONE,
    DEFECT_SEND
) = range(14, 28)

(
    DATE,
    START_DATE,
    END_DATE,
    FIND_BY_DATE,
    SEND_DATE
) = range(28, 33)

END = ConversationHandler.END

DEFAULT_PHOTO_FOLDER = './photos/'

class Role(Enum):
    not_specified = "Не визначено"
    technical_worker = "Технічний працівник"
    sanitary_worker = "Санітарний працівник"


class Status(Enum):
    open = "Відкрито"
    in_process = "В процесі"
    closed = "Закрито"


