from telegram import Update
from telegram.ext import CallbackContext
import constants as con
from buttons import Buttons


def _save_sender(update: Update, context: CallbackContext) -> None:
    sender = update.message.from_user
    context.user_data[con.SENDER_ID] = sender.id
    context.user_data[con.SENDER_USERNAME] = sender.username
    context.user_data[con.SENDER_FIRST_NAME] = sender.first_name
    context.user_data[con.SENDER_LAST_NAME] = sender.last_name


def start(update: Update, context: CallbackContext) -> int:
    """Select an action: Login, Register, Help"""
    text = ('Оберіть дію нижче 👇')
    keyboard = Buttons.get_main_menu()
    
    if context.user_data.get(con.START_OVER):
        query = update.callback_query
        query.answer()
        query.edit_message_text(text=text, reply_markup=keyboard)
    else:
        msg = update.message
        msg.reply_text(text=text, reply_markup=keyboard)
        
        _save_sender(update, context)
    
    context.user_data[con.START_OVER] = False

    return con.SELECTING_ACTION