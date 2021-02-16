from telegram import Update
from telegram.ext import CallbackContext
import constants as con
from enum import Enum
from buttons import Buttons
import os
import requests


class Role(Enum):
    not_specified = 'Not Specified'
    technical_worker = 'Technical Worker'
    sanitary_worker = 'Sanitary Worker'


def _get_user_role(context: CallbackContext):
    url = os.environ.get('BASE_URL') + f'users/me/{context.user_data[con.SENDER_ID]}'
    headers = {
        'Authorization': f'Bearer {context.user_data[con.ACCESS_TOKEN]}'
    }
    res_data = requests.get(url, headers=headers).json()
    return res_data.get("role")


def auth(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    
    sender_id = context.user_data[con.SENDER_ID]
    url = os.environ.get("BASE_URL") + f"users/login/{sender_id}"
    res_data = requests.post(url).json()
    message = res_data.get('message')
    access_token = res_data.get('access_token')

    reply_text = 'Очікуйте на активацію.'
    if not message and access_token:
        reply_text = 'Ви успішно ввійшли!'
        context.user_data[con.ACCESS_TOKEN] = access_token
        role = _get_user_role(context)
        if role == Role.not_specified.value:
            reply_text = 'Ваша роль поки що не визначена. Звернітся до адміністратора.'
        elif role == Role.sanitary_worker.value:
            keyboard = Buttons.add_defect()

    query.answer()
    query.edit_message_text(text=reply_text, reply_markup=keyboard) 

    context.user_data[con.START_OVER] = True

    return con.SHOWING