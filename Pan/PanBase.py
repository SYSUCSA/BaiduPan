# coding=utf-8
import re
import os
import json
import pickle
import base64
import requests
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

from PanError import PanError

from BaiduPan.lib.captcha_verify import verify

from BaiduPan.config import URL_PAN, URL_PASSPORT, URL_PASSPORT_API, URL_INDEX, DIR_DATA, HEADERS_USER_AGENT

pattern_login_error = re.compile(r'auth=&error=(\d+)\'')


class PanBase:
    def __init__(self, username, password, verify_func=verify, flag_save_cookies=True):
        self._session = requests.session()
        self._session.headers.update(HEADERS_USER_AGENT)
        self._username = username
        self._password = password
        self._verify_func = verify_func
        self._flag_save_cookies = flag_save_cookies

        self._token = None
        self._login()

    def _login(self):
        try:
            self._load_cookies()
        except IOError, e:
            # No such file
            if e.errno == 2:
                self._session.get(URL_PAN)
                self._get_token()
                code_string = self._login_check()
                verify_code = self._verify_captcha(code_string)
                login_error = self._login_action(verify_code=verify_code, code_string=code_string)
                if login_error == '0':
                    print '[+] Login success!'
                else:
                    print '[-] Login error. The error code is {}. Please retry.'.format(login_error)
                if self._flag_save_cookies:
                    self._save_cookies()
            else:
                raise PanError(e.strerror)

    def _get_token(self):
        url_get_api = URL_PASSPORT_API.format(act='getapi')
        params = {'tpl': 'pp', 'apiver': 'v3', }
        params_do_not_matter = {
            # params donot matter
            # 'tt': int(time.time() * 1000),
            # 'class': 'login',
            # 'logintype': 'dialogLogin',
            # 'callback': '0',
        }
        params = (params.items() + params_do_not_matter.items())
        r = self._session.get(url_get_api, params=params, allow_redirects=False)
        response = json.loads(r.text.replace('\'', '"'))
        self._token = response['data']['token']

    def _login_check(self):
        url_login_check = URL_PASSPORT_API.format(act='logincheck')
        params = {'apiver': 'v3', }
        params_do_not_matter = {
            # params do not matter
            # 'token': self._token,
            # 'tpl': 'pp',
            # 'tt': int(time.time() * 1000),
            # 'sub_source': 'leadsetpwd',
            # 'username': self._username,
            # 'isphone': 'false',
        }
        params = dict(params.items() + params_do_not_matter.items())
        r = self._session.get(url_login_check, params=params, allow_redirects=False)
        response = json.loads(r.text)
        return response['data']['codeString']

    def _login_action(self, code_string, verify_code):
        pubkey, rsakey = self._get_pubkey()
        password = base64.b64encode(PKCS1_v1_5.new(RSA.importKey(pubkey)).encrypt(self._password))
        url_login = URL_PASSPORT_API.format(act='login')
        data_fixed = {
            'tpl': 'pp',
            'crypttype': '12',
        }
        data_variable = {
            'rsakey': rsakey,
            'mem_pass': 'on' if self._flag_save_cookies else '',
            'verify_code': verify_code,
            'codestring': code_string,
            'username': self._username,
            'password': password,
            'token': self._token,
        }
        data_do_not_matter = {
            # # fixed but do not matter
            # 'apiver': 'v3',
            # 'detect': '1',
            # 'charset': 'UTF-8',
            # 'staticpage': 'https://passport.baidu.com/static/passpc-account/html/v3Jump.html',
            # 'logLoginType': 'pc_loginBasic',
            # 'safeflg': '0',
            # 'quick_user': '0',
            # 'u': 'https://passport.baidu.com/',
            # 'logintype': 'basicLogin',
            # 'loginmerge': 'true',
            #
            # # variable but do not matter:
            # 'tt': int(time.time() * 1000),
            # 'fp_uid': '',
            # 'ppui_logintime': '',
            # 'gid': '',
            # 'fp_info': '',
            # 'dv': '',
            # 'callback': '',
        }
        data = dict(data_fixed.items() + data_variable.items() + data_do_not_matter.items())
        r = self._session.post(url_login, data=data)
        login_error = pattern_login_error.search(r.text).group(1)
        return login_error

    def _verify_captcha(self, code_string):
        if len(code_string) > 0:
            url_gen_image = URL_PASSPORT + '/cgi-bin/genimage' + "?" + code_string
            verify_code = self._verify_func(url_gen_image)
        else:
            verify_code = ""
        return verify_code

    def _get_pubkey(self):
        url_get_pubkey = URL_PASSPORT + '/v2/getpublickey'
        params = {}
        params_do_not_matter = {
            # all params do not matter
            # 'token': self._token,
            # 'tt': int(time.time()*1000),
            # 'apiver': 'v3',
            # 'tpl': 'pp',
            # 'callback': '',
            # 'gid': ''
        }
        params = dict(params.items() + params_do_not_matter.items())
        r = self._session.get(url_get_pubkey, params=params)
        response = json.loads(r.text.replace('\'', '"'))
        pubkey = response['pubkey']
        rsakey = response['key']
        return pubkey, rsakey

    def _save_cookies(self):
        file_cookies = '{}/.{}.cookies'.format(DIR_DATA, self._username)
        with open(file_cookies, 'wb') as f:
            pickle.dump(self._session.cookies, f)
        print '[+] The cookies have saved into file.'

    def _load_cookies(self):
        file_cookies = '{}/.{}.cookies'.format(DIR_DATA, self._username)
        with open(file_cookies, 'rb') as f:
            data = pickle.load(f)
            self._session.cookies = data
        r = self._session.get(URL_INDEX)
        self._save_cookies()
        if self._username.decode('utf-8') in r.text:
            print '[+] Login success with loading cookies!'
        else:
            print '[-] Login failed with loding cookies. Removing the cookies file, then relogin.'
            os.remove(file_cookies)
