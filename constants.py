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
    TAKE_DEFECT,
    CLOSE_DEFECT,
    CHANGE_DEFECT_STATUS
) = range(12)

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
) = range(12, 26)

END = ConversationHandler.END


# Roles constants
class Role(Enum):
    not_specified = "Not Specified"
    technical_worker = "Technical Worker"
    sanitary_worker = "Sanitary Worker"


# Defect status constants
class Status(Enum):
    open = "Open"
    in_process = "In Process"
    closed = "Closed"


