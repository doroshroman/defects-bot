from telegram import Update
from telegram.ext import CallbackContext
import constants as con
from buttons import Buttons
import os
import requests


def register(update: Update, context: CallbackContext) -> int:
    payload = {
        "telegram_id": context.user_data[con.SENDER_ID],
        "first_name": context.user_data[con.SENDER_FIRST_NAME],
        "last_name": context.user_data[con.SENDER_LAST_NAME],
        "username": context.user_data[con.SENDER_USERNAME]
    }
    url = os.environ.get("BASE_URL") + 'users/'
    res_data = requests.post(url, data=payload).json()
    message = res_data.get('message')

    reply_text = ('Ви уже зареєстровані!' if message and 'exist' in message
                    else 'Ваш запит вислано для перевірки, очікуйте на відповідь.')
    
    query = update.callback_query

    query.answer()
    query.edit_message_text(text=reply_text, reply_markup=Buttons.back_to_menu())

    context.user_data[con.START_OVER] = True

    return con.SHOWING