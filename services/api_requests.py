import requests
import os


_base_url = os.environ.get("BASE_URL")


class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token
    
    def __call__(self, r):
        r.headers["Authorization"] = f'Bearer {self.token}'
        return r


class Request:

    @staticmethod
    def register(data):
        url = _base_url + 'users'
        return requests.post(url, data=data)
    
    @staticmethod
    def login(sender_id):
        url = _base_url + f"users/login/{sender_id}"
        return requests.post(url)

    @staticmethod
    def get_user_by_id(sender_id, token):
        url = _base_url + f'users/me/{sender_id}'
        return requests.get(url, auth=BearerAuth(token))

    @staticmethod
    def post_defect(data, files, token):
        url = _base_url + 'defects'
        return requests.post(url, auth=BearerAuth(token), data=data, files=files)
    
    @staticmethod
    def get_defects_by_status(status, token):
        url = _base_url + f'defects/{status}'
        return requests.get(url, auth=BearerAuth(token))
    
    @staticmethod
    def get_defects_by_status_and_date(data, token):
        url = _base_url + f'defects/date'
        return requests.get(url, data=data, auth=BearerAuth(token))

    @staticmethod
    def get_defect_photo(photo_url, token):
        url = _base_url + f'defects/image/{photo_url}'
        return requests.get(url, auth=BearerAuth(token))

    @staticmethod
    def update_defect_status(defect_id, data, token):
        url = _base_url + f'defects/{defect_id}/info'
        return requests.put(url, data=data, auth=BearerAuth(token))
    
    
