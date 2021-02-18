import constants as con
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


class Buttons:
    @staticmethod
    def get_main_menu():
        login_btn = InlineKeyboardButton('🔑 Вхід', callback_data=str(con.LOGIN_ACTION))
        register_btn = InlineKeyboardButton('📝 Реєстрація', callback_data=str(con.REGISTER_ACTION))
        help_btn = InlineKeyboardButton('ℹ️ Допомога', callback_data=str(con.HELP_ACTION))
        keyboard =  InlineKeyboardMarkup([[login_btn, register_btn, help_btn]])

        return keyboard
    
    @staticmethod
    def back_to_menu():
        buttons = [[InlineKeyboardButton(text='🔙 В головне меню', callback_data=str(con.END))]]
        keyboard = InlineKeyboardMarkup(buttons)
        
        return keyboard
    
    @staticmethod
    def add_defect():
        buttons = [
            [InlineKeyboardButton(text='➕ Додати дефект', callback_data=str(con.ADD_DEFECT))],
            [InlineKeyboardButton(text='🔙 В головне меню', callback_data=str(con.END))]
        ]
        keyboard = InlineKeyboardMarkup(buttons)

        return keyboard
    
    @staticmethod
    def cancel():
        buttons = [[InlineKeyboardButton(text='❌ Скасувати', callback_data=str(con.CANCEL))]]
        keyboard = InlineKeyboardMarkup(buttons)
        
        return keyboard