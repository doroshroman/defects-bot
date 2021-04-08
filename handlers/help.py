from telegram import Update, ParseMode
from telegram.ext import CallbackContext
import constants as con
from buttons import Buttons


def help(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    
    text = "Натисніть кнопку <b>Реєстрація</b>, якщо бажаєте користуватися ботом вперше.\n"
    text += "Натисніть <b>Вхід</b>, якщо ви тут не вперше."""
    query.answer()
    query.edit_message_text(text=text, parse_mode=ParseMode.HTML, reply_markup=Buttons.back_to_menu())

    context.user_data[con.START_OVER] = True

    return con.SHOWING