from telegram import Update
from telegram.ext import CallbackContext
import constants as con
from services.defect import Renderer
from services.defect import DefectModel


def defects_in_work(update: Update, context: CallbackContext) -> int:
    user_data = context.user_data
    query = update.callback_query

    status = con.Status.in_process
    token = user_data.get(con.ACCESS_TOKEN)

    defect_model = DefectModel(status, token)
    defects = defect_model.get_defects()

    renderer = Renderer(query, status, defect_model)
    renderer.render(defects)

    return con.CHANGE_DEFECT_STATUS