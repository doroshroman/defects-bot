from telegram import Update, ParseMode
from telegram.ext import CallbackContext
import constants as con
from buttons import Buttons
from utils import Request
import base64
import io


def open_defects(update: Update, context: CallbackContext) -> int:
    user_data = context.user_data
    query = update.callback_query

    status = con.Status.open.name
    token = user_data.get(con.ACCESS_TOKEN)
    response = Request.get_defects_by_status(status, token)
    print("HERE"*10)
    if response.ok:
        defects = response.json()

        query.answer()
        query.edit_message_text(text="Список відкритих дефектів")

        for defect in defects:
            def_text = f"Назва: <b>{defect['title']}</b>\n"
            def_text += (f"Опис: <i>{defect['description']}</i>\n"
                            if 'description' in defect else '') 
            def_text += f"Кімната: {defect['room']}\n" if 'room' in defect else ''
            query.from_user.send_message(text=def_text, parse_mode=ParseMode.HTML)

            # Get defect image
            photo_url = defect.get('attachment')
            if photo_url:
                response = Request.get_defect_photo(photo_url, token).json()
                encoded = response['image_encode'][2:-1]
                decoded = base64.b64decode(encoded)
                photo_file = io.BufferedReader(io.BytesIO(decoded))
                query.from_user.send_photo(photo_file)
            
            keyboard = Buttons.details(defect["id"])
            query.from_user.send_message(text='Виберіть опцію', reply_markup=keyboard)
        
        query.from_user.send_message(text='Вернутися', reply_markup=Buttons.back_to_menu())
    else:
        text = "Поки що немає відкритих дефектів"
        keyboard = Buttons.back_to_menu()
        query.answer()
        query.edit_message_text(text=text, reply_markup=keyboard)

    return con.CHANGE_DEFECT_STATUS


def take_defect(update: Update, context: CallbackContext) -> int:
    data = update.callback_query.data

    defect_id = int(data.replace(con.Status.in_process.value, ''))
    print(defect_id)


