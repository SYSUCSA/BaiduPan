# coding=utf-8
import re
import json
from PanBase import PanBase
from PanError import PanError

from BaiduPan.lib.dict2url import url2dict
from BaiduPan.config import URL_PAN_SHARE_API

pattern_js_yunData = re.compile(r'yunData.setData\(({\S*})\);')


class PanShare(PanBase):
    def save_shared_file(self, short_url, password):
        params_shareid_uk = self._verify_share(short_url, password)
        bds_token, url_referer, file_list = self._get_yun_data(params_shareid_uk)
        self._transfer_share(params_shareid_uk, bds_token, url_referer, file_list)

    def _verify_share(self, short_url, password):
        r = self._session.get(short_url)
        url = URL_PAN_SHARE_API.format(act='verify')
        # params [shareid] and [uk]
        params_shareid_uk = url2dict(r.request.url)
        # all do not matter
        params_fixed = {
            # 'web': '1',
            # 'clienttype': '0',
            # 'app_id': '250528',
            # 'channel': 'chunlei',
        }
        # all do not matter
        params_variable = {
            # 'logid': '',
            # 'bdstoken': 'null',
            # 't': int(time.time()*1000)
        }
        params = dict(params_shareid_uk.items()+params_fixed.items()+params_variable.items())
        data = {'pwd': password, 'vcode': '', 'vcode_str': '', }
        headers_referer = {'Referer': r.request.url}
        r = self._session.post(url, params=params, data=data, headers=headers_referer)
        response = json.loads(r.text)
        errno = response['errno']
        if errno == 0:
            print '[+] Verify success!'
        elif errno == -62:
            raise PanError('[-] Verify failed. Please relogin.')
        return params_shareid_uk

    def _get_yun_data(self, params_shareid_uk):
        url = URL_PAN_SHARE_API.format(act='link')
        r = self._session.get(url, params=params_shareid_uk)
        r.encoding = 'utf-8'
        yun_data = pattern_js_yunData.search(r.text).group(1)
        yun_data = json.loads(yun_data)
        file_list = []
        for data in yun_data['file_list']['list']:
            file_list.append(data['path'].encode('utf-8'),)
        bds_token = yun_data['bdstoken']
        url_referer = r.request.url
        return bds_token, url_referer, file_list

    def _transfer_share(self, params_shareid_uk, bds_token, url_referer, file_list):
        url = URL_PAN_SHARE_API.format(act='transfer')
        uk = params_shareid_uk['uk']
        share_id = params_shareid_uk['share_id']
        params = {'bdstoken': bds_token, 'from': uk, 'shareid': share_id, }
        params_do_not_matter = {
            # params_fixed do not matter
            # 'web': '1',
            # 'clienttype': '0',
            # 'app_id': '250528',
            # 'channel': 'chunlei'

            # params_variable do not matter
            # 'logid': '',
        }
        data = {'path': '/pentest', 'filelist': json.dumps(file_list, ensure_ascii=False), }
        headers_referer = {'Referer': url_referer, }
        params = dict(params.items() + params_do_not_matter.items())
        r = self._session.post(url, params=params, data=data, headers=headers_referer)
        response = json.loads(r.text)
        errno = response['errno']
        if errno == 0:
            print '[+] 保存成功'
        elif errno == 12:
            print '[+] 文件已存在'
        else:
            raise PanError('[-] 未知错误: {}'.format(response))
