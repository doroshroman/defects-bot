import requests
import os


class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token
    
    def __call__(self, r):
        r.headers["Authorization"] = f'Bearer {self.token}'
        return r


class Request:

    @staticmethod
    def register(data):
        url = os.environ.get("BASE_URL") + 'users/'
        return requests.post(url, data=data)
    
    @staticmethod
    def login(sender_id):
        url = os.environ.get("BASE_URL") + f"users/login/{sender_id}"
        return requests.post(url)

    @staticmethod
    def get_user_by_id(sender_id, token):
        url = os.environ.get('BASE_URL') + f'users/me/{sender_id}'
        return requests.get(url, auth=BearerAuth(token))

    @staticmethod
    def post_defect(data, files, token):
        url = os.environ.get('BASE_URL') + 'defects'
        return requests.post(url, auth=BearerAuth(token), data=data, files=files)


