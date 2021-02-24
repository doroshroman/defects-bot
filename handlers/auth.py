from telegram import Update
from telegram.ext import CallbackContext
import constants as con
from buttons import Buttons
from utils import Request


def _get_user_role(context: CallbackContext):
    user_data = context.user_data
    response = Request.get_user_by_id(user_data[con.SENDER_ID], user_data[con.ACCESS_TOKEN]).json()
    return response.get("role")


def auth(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    
    user_data = context.user_data
    sender_id = user_data[con.SENDER_ID]

    response = Request.login(sender_id).json()
    message = response.get('message')
    access_token = response.get('access_token')

    # Default text, keyboard, state in case of error
    reply_text = 'Очікуйте на активацію.'
    keyboard = Buttons.back_to_menu()
    state = con.SHOWING 

    if not message and access_token:
        reply_text = ('Виберіть потрібну опцію' if user_data.get(con.ADD_DEFECT_AGAIN)
                        else 'Ви успішно ввійшли!')

        user_data[con.ACCESS_TOKEN] = access_token

        role = _get_user_role(context)
        if role == con.Role.not_specified.value:
            reply_text = 'Ваша роль поки що не визначена. Звернітся до адміністратора.'
        elif role == con.Role.sanitary_worker.value:
            keyboard = Buttons.get_cleaner_options()
            state = con.DESCRIBING_DEFECT
        elif role == con.Role.technical_worker.value:
            keyboard = Buttons.get_all_options()
            state = con.DESCRIBING_DEFECT
            
    query.answer()
    query.edit_message_text(text=reply_text, reply_markup=keyboard) 

    context.user_data[con.START_OVER] = True

    return state