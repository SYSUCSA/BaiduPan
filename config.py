from lib.get_base_dir import get_base_dir

BASE_DIR = get_base_dir()

TOKEN_TYPE_WEB_SERVER_FLOW = "TOKEN_TYPE_WEB_SERVER_FLOW"
TOKEN_TYPE_USER_AGENT_FLOW = "TOKEN_TYPE_USER_AGENT_FLOW"

RESPONSE_TYPE_TOKEN = "token"
RESPONSE_TYPE_AUTH_CODE = "code"

URL_OPENAPI = "https://openapi.baidu.com"
URL_OAUTH = URL_OPENAPI + "/oauth/2.0"
URL_AUTHORIZE = URL_OAUTH + "/authorize"
URL_TOKEN = URL_OAUTH + "/token"

URL_PCS = "https://c.pcs.baidu.com"
URL_PCS_REST = URL_PCS + "/rest/2.0/pcs/{act}"

PARAMS_AUTH = {
    "scope": "netdisk",
    "redirect_uri": "oob",
    "response_type": "",
    "client_id": "",
}

if __name__ == '__main__':
    from lib.dict2url import dict2url
    print dict2url(PARAMS_AUTH)
