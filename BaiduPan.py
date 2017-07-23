# coding=utf-8
import requests
from config import AUTH_URL


class BaiduPan:
    def __init__(self, api_key):
        self._api_key = api_key
        self._auth_url = AUTH_URL.replace("client_id=", "client_id="+self._api_key)
        self._session = requests.Session()
        self._authorize()

    def _authorize(self):
        msg = 'Please visit:\n{authorize_url}\nAnd authorize this app\n' \
              'Paste the Authorization Code here within 10 minutes.'.format(authorize_url=self._auth_url)
        print msg
        auth_code = raw_input('Input auth_code > ')
        print auth_code
