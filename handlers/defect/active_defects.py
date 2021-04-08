from telegram import Update
from telegram.ext import CallbackContext
import constants as con
from buttons import Buttons
from services.defect import Renderer
from services.defect import DefectModel


def open_defects(update: Update, context: CallbackContext) -> int:
    user_data = context.user_data
    query = update.callback_query

    status = con.Status.open
    token = user_data.get(con.ACCESS_TOKEN)

    defect_model = DefectModel(status, token)
    defects = defect_model.get_defects()

    renderer = Renderer(query, status, defect_model)
    renderer.render(defects)

    return con.CHANGE_DEFECT_STATUS

def open_defects_start_date(update: Update, context: CallbackContext) -> int:
    text = "Введіть початкову дату в форматі день.місяць.рік (01.01.2021)"
    keyboard = Buttons.cancel()

    query = update.callback_query
    query.answer()
    query.edit_message_text(text=text, reply_markup=keyboard)

    return con.END_DATE

def open_defects_end_date(update: Update, context: CallbackContext) -> int:
    start_date = update.message.text
    context.user_data[con.DATE] = {con.START_DATE: start_date}

    text = "Введіть кінцеву дату в форматі день.місяць.рік (01.01.2021)"
    keyboard = Buttons.cancel()

    update.message.reply_text(text=text, reply_markup=keyboard)

    return con.FIND_BY_DATE

def open_defects_send_date(update: Update, context: CallbackContext) -> int:
    end_date = update.message.text
    context.user_data[con.DATE].update({con.END_DATE: end_date})

    text = "Надіслати"
    keyboard = Buttons.done_or_cancel()

    update.message.reply_text(text=text, reply_markup=keyboard)
    return con.SEND_DATE

def open_defects_by_date(update: Update, context: CallbackContext) -> int:
    user_data = context.user_data
    
    token = user_data.get(con.ACCESS_TOKEN)
    
    date = user_data.get(con.DATE)
    start_date = date.get(con.START_DATE)
    end_date = date.get(con.END_DATE)

    status = con.Status.open
    defect_model = DefectModel(status, token)
    defects = defect_model.get_defects_by_date_range(start_date, end_date)
    
    query = update.callback_query
    renderer = Renderer(query, status, defect_model)
    renderer.render(defects)

    return con.CHANGE_DEFECT_STATUS
    




