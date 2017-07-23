# coding=utf-8
import requests

URL_PASSORT = "https://passport.baidu.com/v2/api/?login"


class BaiduPan:
    def __init__(self, username, password):
        self._username = username
        self._password = password
        self._session = requests.Session()

    def _login(self):
        login_data = {
            "username": self._username,
            "password": self._password,
        }
        r = self._session.post(URL_PASSORT, data=login_data)
