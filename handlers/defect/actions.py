from telegram import Update
from telegram.ext import CallbackContext
import constants as con
from services.api_requests import Request


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

def take_defect(update: Update, context: CallbackContext) -> None:
    """Update defect status to in_process"""
    _update_status(update, context, con.Status.in_process)

def close_defect(update: Update, context: CallbackContext) -> None:
    """Update defect status to closed"""
    _update_status(update, context, con.Status.closed)