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

def _update_status(update: Update, context: CallbackContext, status: con.Status):
    query = update.callback_query
    data = query.data
    defect_id = int(data.replace(status.value, ''))

    user_data = context.user_data
    token = user_data.get(con.ACCESS_TOKEN)
    payload = {
        "worker": user_data.get(con.SENDER_ID),
        "status": status.name
    }

    response = Request.update_defect_status(defect_id, payload, token)
    success_text = ('👆 Дефект успішно добавлений в роботу' if status == con.Status.in_process
                        else '👆 Дефект успішно закритий')
    reply_text = success_text if response.ok else "Сталася помилка не сервері"
    
    query.answer()
    query.edit_message_text(text=reply_text)

    return con.DEFECTS_SELECTING_ACTIONS

def take_defect(update: Update, context: CallbackContext) -> None:
    """Update defect status to in_process"""
    _update_status(update, context, con.Status.in_process)

def close_defect(update: Update, context: CallbackContext) -> None:
    """Update defect status to closed"""
    _update_status(update, context, con.Status.closed)



