from lib.get_base_dir import get_base_dir

BASE_DIR = get_base_dir()

TOKEN_TYPE_WEB_SERVER_FLOW = "TOKEN_TYPE_WEB_SERVER_FLOW"
TOKEN_TYPE_USER_AGENT_FLOW = "TOKEN_TYPE_USER_AGENT_FLOW"

RESPONSE_TYPE_TOKEN = "token"
RESPONSE_TYPE_AUTH_CODE = "code"
URL_AUTH = "https://openapi.baidu.com/oauth/2.0/authorize"
PARAM_AUTH = {
    "scope": "netdisk",
    "redirect_uri": "oob",
    "response_type": "",
    "client_id": "",
}
URL_TOKEN = "https://openapi.baidu.com/oauth/2.0/token"
PARAM_TOKEN = {
    "grant_type": "authorization_code",
    "code": "",
    "client_id": "",
    "client_secret": "",
    "redirect_uri": "oob",
}
URL_QUOTA = "https://pcs.baidu.com/rest/2.0/pcs/quota"
PARAM_QUOTA = {
    "method": "info",
    "access_token": "",
}


if __name__ == '__main__':
    from lib.dict2url import dict2url
    print dict2url(PARAM_AUTH)
