#!/usr/bin/env python


import logging
import os
import requests
import constants as con
from handlers.system import start, stop
from handlers.auth import auth
from handlers.register import register
from handlers.help import help
from handlers.defect import add_defect, end_defect

from telegram.ext import (
    Updater,
    CommandHandler,
    ConversationHandler,
    CallbackContext,
    CallbackQueryHandler,
    Filters,
    MessageHandler
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def main() -> None:
    token = os.environ.get("TELEGRAM_TOKEN")
    updater = Updater(token)

    dispatcher = updater.dispatcher

    # collecting data about defect
    defect_conv = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(add_defect, pattern='^' + str(con.ADD_DEFECT) + '$'),
            CallbackQueryHandler(end_defect, pattern='^' + str(con.END) + '$')
        ],
        states={
            con.DEFECT_DESCRIPTION: [
                CallbackQueryHandler(add_defect, pattern='^' + str(con.CANCEL) + '$') 
            ]
        },
        fallbacks=[
            CallbackQueryHandler(end_defect, pattern='^' + str(con.END) + '$')
        ],
        map_to_parent={
            con.END: con.SELECTING_ACTION
        }
    )

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            con.SHOWING: [CallbackQueryHandler(start, pattern='^' + str(con.END) + '$')],
            con.SELECTING_ACTION: [
                CallbackQueryHandler(register, pattern='^' + str(con.REGISTER_ACTION) + '$'),
                CallbackQueryHandler(auth, pattern='^' + str(con.LOGIN_ACTION) + '$'),
                CallbackQueryHandler(help, pattern='^' + str(con.HELP_ACTION) + '$')
            ],
            con.DESCRIBING_DEFECT: [defect_conv]
        },
        fallbacks=[CommandHandler('stop', stop)],
    )

    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()