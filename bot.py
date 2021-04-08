#!/usr/bin/env python


import logging
import os
import constants as con
from handlers.system import start, stop
from handlers.auth import auth
from handlers.register import register
from handlers.help import help
from handlers.defect.new_defect import (
    defect_title,
    end_defect,
    cancel_defect,
    defect_description,
    defect_room,
    defect_photo,
    add_defect,
    send_defect
)
from handlers.defect.actions import take_defect, close_defect
from handlers.defect.active_defects import (
    open_defects,
    open_defects_start_date,
    open_defects_end_date,
    open_defects_send_date,
    open_defects_by_date
) 
from handlers.defect.fixing_defects import defects_in_work

from telegram.ext import (
    Updater,
    CommandHandler,
    ConversationHandler,
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
    new_defect_conv = ConversationHandler(
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

    defects_options = [
        CallbackQueryHandler(open_defects, pattern='^' + str(con.ALL_DEFECTS) + '$'),
        CallbackQueryHandler(defects_in_work, pattern='^' + str(con.DEFECTS_IN_WORK) + '$'),
        CallbackQueryHandler(open_defects_start_date, pattern='^' + str(con.ALL_DEFECTS_BY_DATE) + '$'),
        CallbackQueryHandler(cancel_defect, pattern='^' + str(con.CANCEL_DEFECT) + '$')
    ]

    all_defects_conv = ConversationHandler(
        entry_points=defects_options,
        states={
            con.CHANGE_DEFECT_STATUS: [
                CallbackQueryHandler(take_defect, pattern='^' + str(con.Status.in_process.value) + '[0-9]+$'),
                CallbackQueryHandler(close_defect, pattern='^' + str(con.Status.closed.value) + '[0-9]+$')
            ],
            con.END_DATE: [
                MessageHandler(Filters.text & ~Filters.command, open_defects_end_date)
            ],
            con.FIND_BY_DATE: [
                MessageHandler(Filters.text & ~Filters.command, open_defects_send_date)
            ],
            con.SEND_DATE: [
                CallbackQueryHandler(open_defects_by_date, pattern='^' + str(con.SEND_DATE))
            ]
        },
        fallbacks=defects_options
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
            con.DESCRIBING_DEFECT: [new_defect_conv, all_defects_conv]
        },
        fallbacks=[CommandHandler('stop', stop)],
    )

    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()