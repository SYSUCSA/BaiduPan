from lib.get_base_dir import get_base_dir

DIR_BASE = get_base_dir()
DIR_DATA = DIR_BASE + '/data'

HEADERS_USER_AGENT = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0',
}

# ==========================
# config for Pcs
# ==========================
TOKEN_TYPE_WEB_SERVER_FLOW = 'TOKEN_TYPE_WEB_SERVER_FLOW'
TOKEN_TYPE_USER_AGENT_FLOW = 'TOKEN_TYPE_USER_AGENT_FLOW'

RESPONSE_TYPE_TOKEN = 'token'
RESPONSE_TYPE_AUTH_CODE = 'code'

URL_INDEX = 'https://www.baidu.com'

URL_OPENAPI = 'https://openapi.baidu.com'
URL_OAUTH = URL_OPENAPI + '/oauth/2.0'
URL_AUTHORIZE = URL_OAUTH + '/authorize'
URL_TOKEN = URL_OAUTH + '/token'

URL_PCS = 'https://c.pcs.baidu.com'
URL_PCS_REST = URL_PCS + '/rest/2.0/pcs/{act}'

# ==========================
# config for Pan
# ==========================
URL_PAN = 'https://pan.baidu.com'
URL_PAN_SHARE = URL_PAN + '/share'
URL_PAN_SHARE_API = URL_PAN_SHARE + '/{act}'
URL_PAN_DISK_HOME = URL_PAN + '/disk/home'

URL_PAN_API = URL_PAN + "/api/{act}"

URL_PASSPORT = 'https://passport.baidu.com'
URL_PASSPORT_API = URL_PASSPORT + '/v2/api/?{act}'
