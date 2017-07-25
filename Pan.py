import json
import time
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
            'tt': int(time.time()*1000),
            'logintype': 'dialogLogin',
            'callback': '0',
        }
        r = self._session.get(url, params=params, allow_redirects=False)
        response = json.loads(r.text.replace('\'', '"'))
        self._token = response['data']['token']

    def _login_check(self):
        url = 'https://passport.baidu.com/v2/api/?logincheck'
        params = {
            'token': self._token,
            'tpl': 'mn',
            'apiver': 'v3',
            'tt': int(time.time()*1000),
            'sub_source': 'leadsetpwd',
            'username': self._username,
            'isphone': 'false',
        }
        r = self._session.get(url, params=params, allow_redirects=False)
        response = json.loads(r.text)
        print response
        print r.headers

    def _login_action(self):
        url = 'https://passport.baidu.com/v2/api/?login'
        verify_code = ""
        params_fixed = {

        }
        params_variable = {
            'rsakey': 'TmIto1lsC59WblqycBgkxsBnKRpflaWX',
            'verifycode': verify_code,
            'splogin': 'rate',
            'apiver': 'v3',
            'fp_uid': '4e8b888fe446a6e2b7243ac9f03d0e41',
            'detect': '1',
            'tt': int(time.time()*1000),
            'charset': 'UTF-8',
            'codestring': 'njGeb06f587d4bcf54802b314b75b01308a01905b0611048922',
            'ppui_logintime': '610335',
            'gid': '98A9360-999C-4B30-8304-8EA1189535DE',
            'username': self._username,
            'safeflg': '0',
            'crypttype': '12',
            'staticpage': 'https://www.baidu.com/cache/user/html/v3Jump.html',
            'dv': 'MDExAAoANQALAzkAJAAAAF00AAwCACSI3t7e1-BIHF0TVAZHClUKWglZBjcHWAd3FmUWYQ58GGgbbAgMAgAkiMzMzMXzaz9-MHclZCl2KXkqeiUUJHskVDVGNUItXztLOE8rBwIABJGRkZEMAgALlYeHh46oDGIXexcIAgALk5Dw8JyclbMiTikIAgAehIfc3LCwuadSBkcJThxdEE8QQBNDHCh3KFw1QS1IDQIAHpGRmoGYzI3DhNaX2oXaitmJ1ufXiNenxrXGsd6syAcCAASRkZGRCQIAIYSH2Ni1tbW1tbyJid2c0pXHhsuUy5vImMfzrPOH7pr2kwgCAB6Eh-TkioqKgidzMnw7aShlOmU1ZjZpXQJdKUA0WD0NAgAFkZGRLy8QAgABkRYCACKwxK-fsYi7j7qOvo-3hLOEsYWwhrSFsICwib6Nv4-3hrCEBAIABpKSkJKmkxUCAAiRkZDNtUzepwECAAaRk5OaG7UFAgAEkZGRmhcCABOQkaGhr96Dq4KvyaaK69a43aqKEwIAGpGHh4fvm--f7Nb51qHWoY_tjOWB9Nq51ruUBgIAKJGRkTMzMzMzMzM2YGBgYjw8PDlvb29sbGxsaT8_Pz3Y2Njdi4uLiUwHAgAEkZGRkQ0CAB6RkZFUTRlYFlEDQg9QD18MXAMyAl0CchNgE2QLeR0HAgAEkZGRkQwCACSImpqampDdiciGwZPSn8Cfz5zMk6KSzZLig_CD9Jvpjf2O-Z0NAgAFkZGahYUNAgAFkZiCrKwJAgAhhIfd3ba2tra_oOvrv_6w96Xkqfap-ar6pZHOkeWM-JTxBwIABJGRkZEIAgAJkZUtLQwMBSpGCQIAFJGVIiIDAwMDCiWxsLQaGgkJExMLBwIABJGRkZEJAgAliIpAQKioqKihlcXFkdCe2YvKh9iH14TUi7qK1Yr6m-ib7IPxlQcCAASRkZGRDAIAJIjNzc3E8il9PHI1ZyZrNGs7aDhnVmY5ZhZ3BHcAbx15CXoNaQgCACCGhCUkrq6n79yIyYfAktOewZ7Onc2So5PMk-CV95rzhwkCACyxs4KDzs7OzseLSEgcXRNUBkcKVQpaCVkGNwdYB2oPYgBlF0cmVSZqC2kMYA',
            'logLoginType': 'pc_loginDialog',
            'password': 'DmvXnTh9riHbaCQ7DNnzP6HArRcSLy5AR8SV2RJrsAMxE/ZXXskiRQJRZs2mSqAnwlxF1x0eyV/sBJ3HNbw0yo6alG7uFx+xNQ4j7KF9uZpmOaHKl3gpV1Rr854HWLSSfOmjaTGIMpmKBu6GxW+135+YP85x0oPE1pJjZUACe8k=',
            'isPhone': 'false',
            'tpl': 'mn',
            'logintype': 'dialogLogin',
            'loginmerge': 'true',
            'callback': 'parent.bd__pcbs__xj8cpo',
            'token': self._token,
            'quick_user': '0',
            'u': 'https://www.baidu.com/'
        }
        params = dict(params_fixed.items() + params_variable.items())
