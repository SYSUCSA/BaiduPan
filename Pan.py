# coding=utf-8
import re
import json
# import time
import base64
import requests
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from lib.captcha_verify import verify
from config import URL_PAN, URL_PASSPORT, URL_PASSPORT_API

pattern_login_error = re.compile(r'auth=&error=(\d+)\'')


class PanBase:
    def __init__(self, username, password, verify_func=verify):
        self._session = requests.session()
        self._username = username
        self._password = password
        self._verify_func = verify_func

        self._token = None
        self._login()

    def _login(self):
        self._session.get(URL_PAN)
        self._get_token()
        code_string = self._login_check()
        verify_code = self._verify(code_string)
        login_error = self._login_action(verify_code=verify_code, code_string=code_string)
        if login_error == '0':
            print '[+] Login success!'
        else:
            print '[-] Login error. The error code is {}. Please retry.'.format(login_error)

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
            # 'fp_uid': '68730549f5597e0389835a2d00252b57',
            # 'ppui_logintime': '10309',
            # 'gid': 'B05D9AE-9D99-44FF-BD77-744EE89E1AAE',
            # 'fp_info': '68730549f5597e0389835a2d00252b57002~~~dKgCFqjNYa00Rp0kalEgxddEzgB2F2kbH0~bJ0_ggB2F2kbH0'
            #            '~bpm_PdduUdcDprg0cxBgS3FAXFMqXTKmjNYqXHQergMoVN4ehDEeYNKk-j7ab6OohT7o5yK~YlOacUQqh'
            #            '-OkjN7HbZ7mjJOoBAOomUXkXzAqh-OkjN9vXlMoSHGobjOrBjEG-aOoch7JEN2z0h7JEN2zgl7JmD9FD5EkXiXqX8Aqh'
            #            '-OkjN7HbZFxdsvxduuxdsQxduLg0OEBgS3FAXFMqXTKmjNYqXHQergMoVNBvXUKajpKkSgOoSg7XBSQqATGobjOrBjEG'
            #            'h5EkXiXqX87mjJOoBAOomTGobjOrBjEGh5EkXiXqX87mjJOoBAOomTGobjOrBjEGh5EkXiXqX87mjJOoBAOomTGobjOr'
            #            'BjEGh5EkXiXqX87mjJOoBAOomTGobjOrBjEGh5EkXiXqX87mjJOoBAOomTGobjOrBjEGh5EkXiXqX87mjJOoBAOomTGo'
            #            'bjOrBjEGh5EkXiXqX87mjJOoBAOomTGobjOrBjEGh5EkXiXqX87mjJOoBAOomTGobjOrBjEGh5EkXiXqX87mjJOoBAOo'
            #            'mTGobjOrBjEGh5EkXiXqX87mjJOoBAOomTGobjOrBjEGh5EkXiXqX87mjJOoBAOomTGobjOrBjEGh5EkXiXqX87mjJOo'
            #            'BAOomTGobjOrBjEGh5EkXiXqX8Hw0edsssssm1sssuslutssssssss0ususmsssssssqssss0smssssssssssssss0ss'
            #            'ssssscsssssssssssssssu0uss0ss0DxduyxduwxduBxduWddcIgEOoLUXX2_EgCYoSlQqXJMoODOo1_dxducd~bAGFO'
            #            'CddsfxdsTd-HVOpIpZxdsexdsGxdsRxds',
            # 'dv': 'MDExAAoA3gALAuIAHgAAAF00AAcCAASRkZGRDQIAH5GRsgAaTg9BBlQVWAdYCFsLVGc4ZwpvAmAFdydGNUYIAgAdhYbHxrq6u'
            #       'pj6ru-h5rT1uOe46LvrtIfYh-GO_JEMAgAfiYCAgICYg9eW2J_NjMGewZHCks3-of6L-J3vocCtyAcCAASRkZGRDAIAH4mZmZ'
            #       'mZlL3pqOah87L_oP-v_KzzwJ_Atcaj0Z_-k_YHAgAEkZGRkQwCAB-JgYGBgY0pfTxyNWcmazRrO2g4Z1QLVCFSN0ULagdiDAI'
            #       'AH4nR0dHR2r7qq-Wi8LH8o_ys_6_ww5zDtsWg0pz9kPUHAgAEkZGRkRACAAGRFwIAB5GRnJye95EWAgAjs8esnLKAs4W3j7eE'
            #       'vI-_jr-OvIm-iLmMvIy1jbWFsICxhrUVAgAIkZGQzbRoY2QFAgAEkZGRmgECAAaRk5OaG7UEAgAGkpKQkqaTEwIAKJG1tbXdq'
            #       'd2t3uTL5JT1hvWF6pjswqDBqMy5l_Sb9tmvnbKN4Y7pgO4GAgAokZGRMzMzMzMzMzZ-fn58IiIiJ3FxcXJycnJ3ISEhI8bGxs'
            #       'OVlZWXUgkCACSJih0cEhISEhIV3NyIyYfAktOewZ7Onc2Sof6h1KfCsP6f8pcHAgAEkZGRkQ0CAB2RkZZDWw9OAEcVVBlGGUk'
            #       'aShUmeSZTIEU3eRh1EAcCAASRkZGRDQIAHZGRia214aDuqfu696j3p_Sk-8iXyL3Oq9mX9pv-DQIAHZGRiaW96ajmofOy_6D_'
            #       'r_ys88CfwLDRotGmybvfDAIAI4nNzc3N1Pmt7KLlt_a75LvruOi3hNuE9JXmleKN_5vrmO-LCQIAJouIsLHc3Nzc3P9iYjZ3O'
            #       'X4sbSB_IHAjcywfQB9yF3oYfQ9fPk0-BwIABJGRkZENAgAdkZGyHgZSE10aSAlEG0QURxdIeyR7C2oZah1yAGQJAgAih4TV1F'
            #       '9fX19feVBQBEULTB5fEk0SQhFBHi1yLV4rSSRNOQ',
            # 'callback': 'parent.bd__pcbs__v43r8u',
        }
        data = dict(data_fixed.items() + data_variable.items() + data_do_not_matter.items())
        r = self._session.post(url_login, data=data)
        login_error = pattern_login_error.search(r.text).group(1)
        return login_error

    def _verify(self, code_string):
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
            # 'callback': 'bd__cbs__m2w80x',
            # 'gid': '62C69AC-B402-46D9-8B87-A9425782FD75'
        }
        params = dict(params.items() + params_do_not_matter.items())
        r = self._session.get(url_get_pubkey, params=params)
        response = json.loads(r.text.replace('\'', '"'))
        pubkey = response['pubkey']
        rsakey = response['key']
        return pubkey, rsakey


class Pan(PanBase):
    def __init__(self, username, password, verify_func=verify):
        PanBase.__init__(self, username, password, verify_func)

    def _save_shared_file(self):
        pass
