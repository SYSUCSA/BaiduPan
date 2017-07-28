# coding=utf-8
import os
import json
from PanBase import PanBase
from PanError import PanError
from BaiduPan.config import URL_PAN_API


class PanApi(PanBase):
    def mkdir(self, path, rename_exists=False):
        basename = os.path.basename(path)
        dirname = os.path.dirname(path)
        list_dirs = self.list_dir(dirname)['dirs']
        if basename in list_dirs:
            print '[-] Warning: Path \'{}\' already exists.'.format(path)
        if basename not in list_dirs or rename_exists:
            create_path = self._mkdir_no_matter_already_exists(path)
        else:
            create_path = path
        return create_path

    def _mkdir_no_matter_already_exists(self, path):
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
        print response
        errno = response['errno']
        if errno == 0:
            print '[+] Mkdir \'{}\' successfully!'.format(response['path'])
        elif errno == -6:
            raise PanError('[-] There\'s an important parameter wrong. Please check it.')
        elif errno == 2:
            print PanError('[-] Check the parameter [isdir].')
        else:
            print r.text
            raise PanError('[-] Mkdir unkown error number: {}.'.format(errno))
        return response['path']

    def list_dir(self, dirpath):
        page = 1
        list_files = {
            'dirs': [],
            'files': [],
        }
        while True:
            response_list = self._list_dir_page(dirpath=dirpath, page=page)
            if len(response_list) > 0:
                for file_info in response_list:
                    list_files['dirs' if file_info['isdir'] == 1 else 'files'].append(file_info['server_filename'])
                page += 1
            else:
                break
        return list_files

    def _list_dir_page(self, dirpath, page):
        url = URL_PAN_API.format(act='list')
        params = {
            'showempty': '0',
            'num': '1000',
            'bdstoken': self._token,
            'dir': dirpath,
            'order': 'name',
            'page': page,
            'desc': '0'
        }
        params_do_not_matter = {
            # 'web': '1',
            # 'clienttype': '0',
            # 'app_id': '250528',
            # 'logid': '',
            # 'channel': 'chunlei',
        }
        params = dict(params.items() + params_do_not_matter.items())
        r = self._session.get(url, params=params)
        response = json.loads(r.text)
        errno = response['errno']
        if errno == 0:
            pass
        elif errno == 1:
            print '[-] Warning: unkown erron 1. Retry list the dir of page {}.'.format(page)
            return self._list_dir_page(dirpath, page)
        else:
            print response
            raise PanError('[-] Dir list error: {}.'.format(errno))
        return response['list']
