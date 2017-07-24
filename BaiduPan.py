# coding=utf-8
import json
import requests
from lib.dict2url import dict2url, url2dict
from config import URL_AUTH, PARAM_AUTH, RESPONSE_TYPE_TOKEN, RESPONSE_TYPE_AUTH_CODE, URL_TOKEN, PARAM_TOKEN
from config import TOKEN_TYPE_WEB_SERVER_FLOW, TOKEN_TYPE_USER_AGENT_FLOW
from config import URL_QUOTA, PARAM_QUOTA


class AuthorizeError(Exception):
    def __init__(self, v):
        self.value = v

    def __str__(self):
        return self.value


class BaiduPanBase:
    def __init__(self, access_token=None, token_type=None, api_key=None, secret_key=None, auth_code=None):
        self._session = requests.Session()

        self._access_token = access_token
        self._token_type = token_type
        self._api_key = api_key
        self._secret_key = secret_key
        self._auth_code = auth_code

        if self._access_token is None:
            self._get_access_token()

    def _get_access_token(self):
        if self._auth_code is None:
            if self._token_type is None:
                self._token_type = TOKEN_TYPE_USER_AGENT_FLOW
        else:
            self._token_type = TOKEN_TYPE_WEB_SERVER_FLOW

        if self._api_key is None:
            msg = "\nThe parameter [api_key] is necessary.\nYou can get your api_key by creating app in here:\n" \
              "http://developer.baidu.com/console#app/"
            print msg
            self._api_key = raw_input("Input API Key > ")

        if self._token_type is TOKEN_TYPE_WEB_SERVER_FLOW:
            if self._secret_key is None:
                self._secret_key = raw_input("Input Secret Key > ")
            if self._auth_code is None:
                self._authorize()
            self._get_access_token_web_server_flow()
        elif self._token_type is TOKEN_TYPE_USER_AGENT_FLOW:
            self._get_access_token_user_agent_flow()

    def _get_access_token_web_server_flow(self):
        param_token = PARAM_TOKEN
        param_token["code"] = self._auth_code
        param_token["client_id"] = self._api_key
        param_token["client_secret"] = self._secret_key
        r = self._session.get(URL_TOKEN, params=PARAM_TOKEN)
        data = json.loads(r.text)
        print r.request.url
        self._access_token = data["access_token"]

    def _authorize(self):
        auth_param = PARAM_AUTH
        auth_param["client_id"] = self._api_key
        auth_param["response_type"] = RESPONSE_TYPE_AUTH_CODE
        auth_url = URL_AUTH + "?" + dict2url(auth_param)
        msg = 'Please visit:\n{authorize_url}\nAnd authorize this app\n' \
              'Paste the Authorization Code here within 10 minutes.'.format(authorize_url=auth_url)
        print msg
        auth_code = raw_input('Input auth_code > ')
        self._auth_code = auth_code

    def _get_access_token_user_agent_flow(self):
        auth_param = PARAM_AUTH
        auth_param["client_id"] = self._api_key
        auth_param["response_type"] = RESPONSE_TYPE_TOKEN
        auth_url = URL_AUTH + "?" + dict2url(auth_param)
        msg = 'Please visit:\n{authorize_url}\nAnd authorize this app\n' \
              'Paste the url or params here within 10 minutes.'.format(authorize_url=auth_url)
        print msg
        url = raw_input("Input url or params > ")
        data = url2dict(url)
        self._access_token = data["access_token"]


class BaiduPan(BaiduPanBase):
    def __init__(self, app_name, access_token=None, token_type=None, api_key=None, secret_key=None, auth_code=None):
        BaiduPanBase.__init__(self, access_token, token_type, api_key, secret_key, auth_code)
        self._appname = app_name

    def quota(self):
        param_quota = PARAM_QUOTA
        param_quota["access_token"] = self._access_token
        r = self._session.get(URL_QUOTA, params=param_quota)
        print r.request.url
        print r.text

    def file_list(self):
        url = "https://pcs.baidu.com/rest/2.0/pcs/file"
        param = {
            "method": "list",
            "access_token": self._access_token,
            "path": "/apps/" + self._appname
        }
        r = self._session.get(url, params=param)
        print r.text
