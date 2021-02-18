from telegram import Update
from telegram.ext import CallbackContext
import constants as con
from buttons import Buttons
from .system import start
from .auth import auth

from io import BytesIO


def defect_title(update: Update, context: CallbackContext) -> int:
    text = "Введіть назву пошкодження"
    keyboard = Buttons.cancel()

    query = update.callback_query
    query.answer()
    query.edit_message_text(text=text, reply_markup=keyboard)
    
    return con.DEFECT_DESCRIPTION

def defect_description(update: Update, context: CallbackContext) -> int:
    title = update.message.text
    context.user_data[con.DEFECT] = {con.DEFECT_TITLE: title}
    
    text = "Введіть опис пошкодження"
    keyboard = Buttons.cancel()
    
    update.message.reply_text(text=text, reply_markup=keyboard)

    return con.DEFECT_ROOM

def defect_room(update: Update, context: CallbackContext) -> int:
    description = update.message.text
    context.user_data[con.DEFECT].update({con.DEFECT_DESCRIPTION: description})

    text = "Введіть кімнату"
    keyboard = Buttons.cancel()

    update.message.reply_text(text=text, reply_markup=keyboard)

    return con.DEFECT_PHOTO

def defect_photo(update: Update, context: CallbackContext) -> int:
    room = update.message.text
    context.user_data[con.DEFECT].update({con.DEFECT_ROOM: room})

    text = "Завантажте фото"
    keyboard = Buttons.cancel()

    update.message.reply_text(text=text, reply_markup=keyboard)

    return con.DEFECT_DONE

def add_defect(update: Update, context: CallbackContext) -> int:
    photo_file = update.message.photo[-1].get_file()
    photo_stream = BytesIO(photo_file.download_as_bytearray())
    

def end_defect(update: Update, context: CallbackContext) -> int:
    context.user_data[con.START_OVER] = True
    start(update, context)
    
    return con.END

def cancel_defect(update: Update, context: CallbackContext) -> int:
    context.user_data[con.ADD_DEFECT_AGAIN] = True
    auth(update, context)
    
    return con.CANCEL
    