from telegram import Update
from telegram.ext import CallbackContext
import constants as con
from buttons import Buttons
from ..system import start
from ..auth import auth
from services.api_requests import Request

import os


def _remove_defect_cache(context: CallbackContext) -> None:
    """Removes defect data from context.user_data
       removes folder with defect photos too
    """
    user_data = context.user_data

    defect_state = con.DEFECT
    defect = user_data.get(defect_state)
    defect_photo = defect.get(con.DEFECT_PHOTO) if defect else None
    if defect_photo and os.path.isfile(defect_photo):
        os.remove(defect_photo)

    # delete empty folder
    photo_folder = os.environ.get('FILE_CUSTOM_PATH') or con.DEFAULT_PHOTO_FOLDER
    if os.path.isdir(photo_folder) and not len(os.listdir(photo_folder)):
        os.rmdir(photo_folder)
    
    if defect_state in user_data:
        del user_data[defect_state]
    

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

    photos_directory = os.environ.get('FILE_CUSTOM_PATH') or con.DEFAULT_PHOTO_FOLDER
    if not os.path.exists(photos_directory):
        os.makedirs(photos_directory)

    custom_path = photos_directory + photo_file.file_unique_id + '.jpg'
    photo_file.download(custom_path=custom_path)
    context.user_data[con.DEFECT].update({con.DEFECT_PHOTO: custom_path})

    text = "Надіслати"
    keyboard = Buttons.done_or_cancel()
    update.message.reply_text(text=text, reply_markup=keyboard)
    
    return con.DEFECT_SEND

def send_defect(update: Update, context: CallbackContext) -> None:
    user_data = context.user_data
    defect = user_data.get(con.DEFECT)
    token = user_data.get(con.ACCESS_TOKEN)
    payload = {
        "created_by": user_data.get(con.SENDER_ID),
        "title": defect.get(con.DEFECT_TITLE),
        "description": defect.get(con.DEFECT_DESCRIPTION),
        "room": defect.get(con.DEFECT_ROOM) 
    }
    photo_file = open(defect.get(con.DEFECT_PHOTO), 'rb')
    files = {
        "attachment": photo_file
    }
    response = Request.post_defect(payload, files, token)
    photo_file.close()

    _remove_defect_cache(context)

    text = ("Дефект успішно додано!" if response.ok 
                else "Сталась помилка на сервері")
    
    
    query = update.callback_query
    keyboard = Buttons.back_to_menu()

    query.answer()
    query.edit_message_text(text=text, reply_markup=keyboard)


def end_defect(update: Update, context: CallbackContext) -> int:
    context.user_data[con.START_OVER] = True
    start(update, context)
    
    return con.END

def cancel_defect(update: Update, context: CallbackContext) -> int:
    context.user_data[con.ADD_DEFECT_AGAIN] = True

    _remove_defect_cache(context)
    auth(update, context)
    
    return con.CANCEL_DEFECT
    