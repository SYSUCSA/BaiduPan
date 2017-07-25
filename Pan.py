import time
import requests
from config import URL_PAN


class PanBase:
    def __init__(self, username, password):
        self._session = requests.session()
        self._username = username
        self._password = password
        self._login()

    def _login(self):
        self._session.get(URL_PAN)

    def _get_token(self):
        url = "https://passport.baidu.com/v2/api/?getapi"
        params = {
            "tpl": "mn",
            "apiver": "v3",
            "class": "login",
            "tt": time.time(),
            "logintype": "dialogLogin",
            "callback": "0",
        }
        r = self._session.get(url, params=params, allow_redirects=False)
        print r.request.headers
        print r.url
        print r.status_code
        print r.text


if __name__ == '__main__':
    # pan_base = PanBase(username=None, password=None)
    # from urlparse import urlparse
    pan_base = PanBase(username=None, password=None)
    pan_base._get_token()
