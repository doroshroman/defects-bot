import constants as con
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


class Buttons:

    @staticmethod
    def get_main_menu():
        login_btn = InlineKeyboardButton('🔑 Вхід', callback_data=str(con.LOGIN_ACTION))
        register_btn = InlineKeyboardButton('📝 Реєстрація', callback_data=str(con.REGISTER_ACTION))
        help_btn = InlineKeyboardButton('ℹ️ Допомога', callback_data=str(con.HELP_ACTION))
        buttons = [[login_btn, register_btn, help_btn]]
        return InlineKeyboardMarkup(buttons)
    
    @staticmethod
    def back_to_menu():
        buttons = [[InlineKeyboardButton(text='🔙 В головне меню', callback_data=str(con.END))]]
        return InlineKeyboardMarkup(buttons)
    
    @staticmethod
    def get_cleaner_options():
        buttons = [
            [InlineKeyboardButton(text='➕ Додати дефект', callback_data=str(con.ADD_DEFECT))],
            [InlineKeyboardButton(text='🔙 В головне меню', callback_data=str(con.END))]
        ]
        return InlineKeyboardMarkup(buttons)
    
    @staticmethod
    def get_all_options():
        buttons = [
            [InlineKeyboardButton(text='➕ Додати дефект', callback_data=str(con.ADD_DEFECT))],
            [InlineKeyboardButton(text='📖 Неопрацьовані дефекти', callback_data=str(con.ALL_DEFECTS))],
            [InlineKeyboardButton(text='📅 Неопрацьовані дефекти за датою', callback_data='test')],
            [InlineKeyboardButton(text='⚙️ Дефекти в роботі', callback_data=str(con.DEFECTS_IN_WORK))],
            [InlineKeyboardButton(text='🔙 В головне меню', callback_data=str(con.END))]
        ]
        return InlineKeyboardMarkup(buttons)

    @staticmethod
    def done():
        buttons = [
            [InlineKeyboardButton(text='✅ Готово', callback_data=str(con.DEFECT_SEND))]
        ]
        return InlineKeyboardMarkup(buttons)

    @staticmethod
    def cancel():
        buttons = [[InlineKeyboardButton(text='❌ Скасувати', callback_data=str(con.CANCEL_DEFECT))]]
        return InlineKeyboardMarkup(buttons)
    
    @staticmethod
    def details(id):
        buttons = [
            [InlineKeyboardButton(text='↗️ В роботі', callback_data=con.Status.in_process.value + str(id))],
            [InlineKeyboardButton(text='🔒 Закрити', callback_data=con.Status.closed.value + str(id))]
        ]
        return InlineKeyboardMarkup(buttons)
    
    @staticmethod
    def close(id):
        return InlineKeyboardMarkup([
            [InlineKeyboardButton(text='🔒 Закрити', callback_data=con.Status.closed.value + str(id))]
        ])
