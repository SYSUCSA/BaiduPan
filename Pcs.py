# coding=utf-8
import json
import sys
import requests
import os.path
from lib.dict2url import dict2url, url2dict
from config import URL_AUTHORIZE, URL_PCS_REST, URL_TOKEN
from config import RESPONSE_TYPE_TOKEN, RESPONSE_TYPE_AUTH_CODE, TOKEN_TYPE_WEB_SERVER_FLOW, TOKEN_TYPE_USER_AGENT_FLOW


class AuthorizeError(Exception):
    def __init__(self, v):
        self.value = v

    def __str__(self):
        return self.value


class PcsBase:
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
        params_token = {
            "grant_type": "authorization_code",
            "code": self._auth_code,
            "client_id": self._api_key,
            "client_secret": self._secret_key,
            "redirect_uri": "oob",
        }
        r = self._session.get(URL_TOKEN, params=params_token)
        data = json.loads(r.text)
        print r.request.url
        self._access_token = data["access_token"]

    def _authorize(self):
        auth_code = self._oauth(response_type=RESPONSE_TYPE_AUTH_CODE, paste="auth_code")
        self._auth_code = auth_code

    def _get_access_token_user_agent_flow(self):
        url = self._oauth(response_type=RESPONSE_TYPE_TOKEN, paste="url or params contains access_token")
        data = url2dict(url)
        self._access_token = data["access_token"]

    def _oauth(self, response_type, paste):
        params_oauth = {
            "scope": "netdisk",
            "redirect_uri": "oob",
            "response_type": response_type,
            "client_id": self._api_key,
        }
        oauth_url = URL_AUTHORIZE + "?" + dict2url(params_oauth)
        msg = 'Please visit:\n{authorize_url}\nAnd authorize this app.'.format(authorize_url=oauth_url)
        print msg
        data = raw_input('Paste the {paste} here:\n> '.format(paste=paste))
        return data


class PcsApi(PcsBase):
    def __init__(self, app_name, access_token=None, token_type=None, api_key=None, secret_key=None, auth_code=None):
        PcsBase.__init__(self, access_token, token_type, api_key, secret_key, auth_code)
        self._appname = app_name

    def quota(self):
        params_quota = {
            "method": "info",
            "access_token": self._access_token,
        }
        r = self._session.get(URL_PCS_REST.format(act="quota"), params=params_quota)
        print r.text

    def file_list(self):
        params = {
            "method": "list",
            "access_token": self._access_token,
            "path": "/apps/" + self._appname
        }
        r = self._session.get(URL_PCS_REST.format(act="file"), params=params)
        print r.content

    def upload_single_file(self, path, files, ondup="overwrite"):
        params = {
            "method": "upload",
            "access_token": self._access_token,
            "path": "/apps/" + self._appname + path,
            "ondup": ondup
        }
        r = self._session.post(URL_PCS_REST.format(act="file"), params=params, files=files)
        print r.text

    def upload_tmp_file(self, files):
        params = {
            "method": "upload",
            "access_token": self._access_token,
            "type": "tmpfile"
        }
        r = self._session.post(URL_PCS_REST.format(act="file"), params=params, files=files)
        print r.text
        return r.content[8:40]

    def create_super_file(self, path, param, ondup="overwrite"):
        params = {
            "method": "createsuperfile",
            "access_token": self._access_token,
            "path": "/apps/" + self._appname + path,
            "ondup": ondup
        }
        r = self._session.post(URL_PCS_REST.format(act="file"), params=params, data={'param':json.dumps(param)})
        print r.text

    def download_single_file(self, path):
        URL_PCS = "https://d.pcs.baidu.com"
        params = {
            "method": "download",
            "access_token": self._access_token,
            "path": path,
        }
        r = self._session.get(URL_PCS_REST.format(act="file"), params=params)
        filename = os.path.basename(path)
        if not os.path.exists("download/"):
            os.mkdir("download/")
        file_path = "download/" + filename
        with open(file_path,'w') as f:
            f.write(r.content)

class Pcs(PcsApi):
    def __init__(self, app_name, access_token=None, token_type=None, api_key=None, secret_key=None, auth_code=None):
        PcsApi.__init__(self, app_name, access_token, token_type, api_key, secret_key, auth_code)

    def list(self):
        self.file_list()

    def download(self, path):
        self.download_single_file(path)

    def split_file(self, file_path):
        todir = "tmpfiles/"
        chunksize = int(1.5*1024*1024*1024)
        if not os.path.exists(todir):  # check whether todir exists or not
            os.mkdir(todir)
        else:
            for fname in os.listdir(todir):
                os.remove(os.path.join(todir, fname))
        partnum = 0
        superfile = open(file_path, 'rb')  # open the file
        while True:
            chunk = superfile.read(chunksize)
            if not chunk:  # check the chunk is empty
                break
            partnum += 1
            filename = os.path.join(todir, ('part%04d' % partnum))
            fileobj = open(filename, 'wb')  # make partfile
            fileobj.write(chunk)  # write data into partfile
            fileobj.close()
        return partnum

    def upload(self, path, file_path, ondup="overwrite"):
        filesize = os.path.getsize(file_path)
        if filesize <= 2*1024*1024*1024:
            files = {'file': open(file_path, 'rb')}
            self.upload_single_file(path, files, ondup)
        else:
            try:
                parts = self.split_file(file_path) #split file to tmp files
            except:
                print('Error during split:')
                print(sys.exc_info()[0], sys.exc_info()[1])
            else:
                print('split finished:', parts, 'parts are in tmpfiles/')
            block_list = []
            for fname in os.listdir("tmpfiles/"):
                files = {'file': open(os.path.join("tmpfiles/", fname), 'rb')}
                md5 = self.upload_tmp_file(files)
                block_list.append(md5)# upload tmp files
            param = {"block_list": block_list}
            print param
            self.create_super_file(path, param, ondup)

    def bulk_upload(self, folder_path, ondup="overwrite"):
        for fname in os.listdir(folder_path):
            file_path = os.path.join(folder_path, fname)
            self.upload("/"+fname, file_path, ondup)

    





