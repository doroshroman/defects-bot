#!/usr/bin/env python


import logging
import os
import requests
import constants as con
from handlers.start import start
from handlers.auth import auth
from handlers.register import register
from handlers.help import help

from telegram.ext import (
    Updater,
    CommandHandler,
    ConversationHandler,
    CallbackContext,
    CallbackQueryHandler
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

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            con.SHOWING: [CallbackQueryHandler(start, pattern='^' + str(con.END) + '$')],
            con.SELECTING_ACTION: [
                CallbackQueryHandler(register, pattern='^' + str(con.REGISTER_ACTION) + '$'),
                CallbackQueryHandler(auth, pattern='^' + str(con.LOGIN_ACTION) + '$'),
                CallbackQueryHandler(help, pattern='^' + str(con.HELP_ACTION) + '$')
            ]
        },
        fallbacks=[CommandHandler('start', start)],
    )

    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()