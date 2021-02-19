#!/usr/bin/env python


import logging
import os
import requests
import constants as con
from handlers.system import start, stop
from handlers.auth import auth
from handlers.register import register
from handlers.help import help
from handlers.defect import (
    defect_title,
    end_defect,
    cancel_defect,
    defect_description,
    defect_room,
    defect_photo,
    add_defect,
    send_defect
)

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
            CallbackQueryHandler(defect_title, pattern='^' + str(con.ADD_DEFECT) + '$'),
            CallbackQueryHandler(end_defect, pattern='^' + str(con.END) + '$')
        ],
        states={
            con.DEFECT_DESCRIPTION: [
                MessageHandler(Filters.text & ~Filters.command, defect_description)
            ],
            con.DEFECT_ROOM: [
                MessageHandler(Filters.text & ~Filters.command, defect_room)
            ],
            con.DEFECT_PHOTO: [
                MessageHandler(Filters.text & ~Filters.command, defect_photo)
            ],
            con.DEFECT_DONE: [
                MessageHandler(Filters.photo, add_defect)
            ],
            con.DEFECT_SEND: [
                CallbackQueryHandler(send_defect, pattern='^' + str(con.DEFECT_SEND) + '$')
            ]
            
        },
        fallbacks=[
            CallbackQueryHandler(cancel_defect, pattern='^' + str(con.CANCEL_DEFECT) + '$'),
            CallbackQueryHandler(end_defect, pattern='^' + str(con.END) + '$')
        ],
        map_to_parent={
            con.END: con.SELECTING_ACTION,
            con.CANCEL_DEFECT: con.DESCRIBING_DEFECT
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