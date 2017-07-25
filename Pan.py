import json
import time
from urllib import quote
import requests
from config import URL_PAN


class PanBase:
    def __init__(self, username, password):
        self._session = requests.session()
        self._username = username
        self._password = password
        self._token = None
        self._login()

    def _login(self):
        self._session.get(URL_PAN)
        self._get_token()

    def _get_token(self):
        url = 'https://passport.baidu.com/v2/api/?getapi'
        params = {
            'tpl': 'mn',
            'apiver': 'v3',
            'class': 'login',
            'tt': time.time(),
            'logintype': 'dialogLogin',
            'callback': '0',
        }
        r = self._session.get(url, params=params, allow_redirects=False)
        response = json.loads(r.text.replace('\'', '"'))
        self._token = response['data']['token']

    def _login_check(self):
        url = 'https://passport.baidu.com/v2/api/?login'
        params = {
            'token': self._token,
            'tpl': 'mn',
            'apiver': 'v3',
            'tt': time.time(),
            'sub_source': 'leadsetpwd',
            'username': quote(self._username),
            'isphone': 'false',
        }
        r = self._session.get(url, params=params, allow_redirects=False)
        print r.text
