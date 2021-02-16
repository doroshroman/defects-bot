from telegram.ext import ConversationHandler

# State constants
(
    SELECTING_ACTION,
    LOGIN_ACTION,
    REGISTER_ACTION,
    HELP_ACTION,
    SHOWING,
    ADD_DEFECT
) = range(6)

# user context constants
(
    START_OVER,
    SENDER_ID,
    SENDER_USERNAME,
    SENDER_FIRST_NAME,
    SENDER_LAST_NAME,
    ACCESS_TOKEN
) = range(6, 12)

END = ConversationHandler.END


