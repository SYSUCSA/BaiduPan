import json
from PanBase import PanBase
from PanError import PanError
from BaiduPan.config import URL_PAN_API


class PanApi(PanBase):
    def mkdir(self, path):
        url = URL_PAN_API.format(act='create')
        params = {
            'a': 'commit',
            'bdstoken': self._token,
        }
        params_do_not_matter = {
            # 'web': '1',
            # 'clienttype': '0',
            # 'app_id': '250528',
            # 'channel': 'chunlei'
            # 'logid': '',
        }
        params = dict(params.items() + params_do_not_matter.items())
        block_list = []
        data = {
            'path': path,
            'isdir': '1',
            'block_list': block_list,
        }
        r = self._session.post(url, params=params, data=data)
        response = json.loads(r.text)
        errno = response['errno']
        if errno == -6:
            print '[-] There\'s an important parameter wrong. Please check it.'
        elif errno == 2:
            print '[-] Check the parameter [isdir].'
        else:
            raise PanError('[-] Mkdir error number: {}.'.format(errno))
