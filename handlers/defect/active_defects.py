from telegram import Update
from telegram.ext import CallbackContext
import constants as con
from services.defect_renderer import Renderer


def open_defects(update: Update, context: CallbackContext) -> int:
    user_data = context.user_data
    query = update.callback_query

    status = con.Status.open
    token = user_data.get(con.ACCESS_TOKEN)
    
    renderer = Renderer(query, status, token)
    renderer.render()

    return con.CHANGE_DEFECT_STATUS



