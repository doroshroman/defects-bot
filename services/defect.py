from telegram import ParseMode
from .api_requests import Request
import constants as con
from buttons import Buttons
import io, base64
from datetime import datetime as dt
from email.utils import format_datetime


class DefectModel:
    def __init__(self, status, token):
        self.status = status
        self.token = token
    
    def get_defects(self):
        response = Request.get_defects_by_status(self.status.name, self.token)
        return response.json() if response.ok else []
    
    def get_defects_by_date_range(self, start_date, end_date):
        try:
            start_day, start_month, start_year = [int(sd) for sd in start_date.split('.')]
            end_day, end_month, end_year = [int(sd) for sd in end_date.split('.')]
            start_date_dt = dt(start_year, start_month, start_day)
            end_date_dt = dt(end_year, end_month, end_day)

            payload={
                "status": self.status.name,
                "open_date": format_datetime(start_date_dt),
                "close_date": format_datetime(end_date_dt)
            }
            response = Request.get_defects_by_status_and_date(payload, self.token)
            return response.json() if response.ok else []
        
        except ValueError:
            return []
        

class Renderer:
    def __init__(self, query, status, defects):
        self.query = query
        self.status = status
        self.defects = defects
            
    def render(self):
        success_text = ("Список дефектів в роботі" if self.status == con.Status.in_process
                        else "Список відкритих дефектів")
        header_text = success_text if self.defects else 'Поки що немає дефектів'

        self.query.answer()
        self.query.edit_message_text(header_text)

        for defect in self.defects:
            def_text = f"Назва: <b>{defect['title']}</b>\n"
            def_text += (f"Опис: <i>{defect['description']}</i>\n"
                            if 'description' in defect else '') 
            def_text += f"Кімната: {defect['room']}\n" if 'room' in defect else ''
            self.query.from_user.send_message(text=def_text, parse_mode=ParseMode.HTML)

            # Get defect image
            photo_url = defect.get('attachment')
            if photo_url:
                response = Request.get_defect_photo(photo_url, self.token).json()
                encoded = response['image_encode'][2:-1]
                decoded = base64.b64decode(encoded)
                photo_file = io.BufferedReader(io.BytesIO(decoded))
                self.query.from_user.send_photo(photo_file)

            def_id = defect["id"]
            keyboard = (Buttons.close(def_id) if self.status == con.Status.in_process 
                        else Buttons.details(def_id) if self.status == con.Status.open
                        else Buttons.back_to_menu())
            
            self.query.answer()
            self.query.from_user.send_message(text='Виберіть опцію', reply_markup=keyboard)

        self.query.from_user.send_message(text='Вернутися', reply_markup=Buttons.back_to_menu())
            


