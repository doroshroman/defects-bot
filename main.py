#!/usr/bin/env python


import logging
import os
import requests

from telegram import (
    ReplyKeyboardRemove, Update,
    InlineKeyboardMarkup, InlineKeyboardButton
)
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

SELECTING_ACTION = range(1)
LOGIN_ACTION, REGISTER_ACTION, HELP_ACTION = range(4, 7)
SHOWING = range(8, 9)
START_OVER = 10
SENDER_ID, SENDER_USERNAME, SENDER_FIRST_NAME, SENDER_LAST_NAME = range(11, 15) 
END = ConversationHandler.END

def _get_sender(update: Update, context: CallbackContext):
    sender = update.message.from_user
    return sender

def start(update: Update, context: CallbackContext) -> int:
    """Select an action: Login, Register, Help"""
    text = ('Оберіть дію нижче 👇')
    
    login_btn = InlineKeyboardButton('🔑 Вхід', callback_data=str(LOGIN_ACTION))
    register_btn = InlineKeyboardButton('📝 Реєстрація', callback_data=str(REGISTER_ACTION))
    help_btn = InlineKeyboardButton('ℹ️ Допомога', callback_data=str(HELP_ACTION))

    keyboard =  InlineKeyboardMarkup([[login_btn, register_btn, help_btn]])

    if context.user_data.get(START_OVER):
        query = update.callback_query
        query.answer()
        query.edit_message_text(text=text, reply_markup=keyboard)
    else:
        msg = update.message
        msg.reply_text(
            'Привіт!'
        )
        msg.reply_text(text=text, reply_markup=keyboard)

        sender = _get_sender(update, context)
        context.user_data[SENDER_ID] = sender.id
        context.user_data[SENDER_USERNAME] = sender.username
        context.user_data[SENDER_FIRST_NAME] = sender.first_name
        context.user_data[SENDER_LAST_NAME] = sender.last_name
    
    context.user_data[START_OVER] = False

    return SELECTING_ACTION


def register(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    buttons = [[InlineKeyboardButton(text='🔙 Назад', callback_data=str(END))]]
    keyboard = InlineKeyboardMarkup(buttons)

    payload = {
        "telegram_id": context.user_data[SENDER_ID],
        "first_name": context.user_data[SENDER_FIRST_NAME],
        "last_name": context.user_data[SENDER_LAST_NAME],
        "username": context.user_data[SENDER_USERNAME]
    }
    url = os.environ.get("BASE_URL") + 'users/'
    res_data = requests.post(url, data=payload).json()
    message = res_data.get('message')

    reply_text = ('Ви уже зареєстровані!' if message and 'exist' in message
                    else 'Ваш запит вислано для перевірки, очікуйте на відповідь.')
    
    query.answer()
    query.edit_message_text(text=reply_text, reply_markup=keyboard)

    context.user_data[START_OVER] = True

    return SHOWING

def cancel(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Bye! I hope we can talk again some day.', reply_markup=ReplyKeyboardRemove()
    )

    return END


def main() -> None:
    # Create the Updater and pass it your bot's token.
    token = os.environ.get("TELEGRAM_TOKEN")
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            SHOWING: [CallbackQueryHandler(start, pattern='^' + str(END) + '$')],
            SELECTING_ACTION: [
                CallbackQueryHandler(register, pattern='^' + str(REGISTER_ACTION) + '$')
            ]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()