from telegram import Update
from telegram.ext import CallbackContext
import constants as con
from buttons import Buttons
from .system import start


def add_defect(update: Update, context: CallbackContext) -> int:
    text = "Введіть опис пошкодження"
    keyboard = Buttons.cancel()

    query = update.callback_query
    query.answer()
    query.edit_message_text(text=text, reply_markup=keyboard)
    

def end_defect(update: Update, context: CallbackContext) -> int:
    context.user_data[con.START_OVER] = True
    start(update, context)
    
    return con.END
    