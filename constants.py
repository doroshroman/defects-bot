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
    DEFECT_DESCRIPTION,
    CANCEL
) = range(9)

# user context constants
(
    START_OVER,
    SENDER_ID,
    SENDER_USERNAME,
    SENDER_FIRST_NAME,
    SENDER_LAST_NAME,
    ACCESS_TOKEN,
) = range(9, 15)

END = ConversationHandler.END

# Roles constants
class Role(Enum):
    not_specified = 'Not Specified'
    technical_worker = 'Technical Worker'
    sanitary_worker = 'Sanitary Worker'


