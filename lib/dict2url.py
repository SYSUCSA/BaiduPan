from urlparse import urlparse, parse_qs


def dict2url(d):
    return "&".join([k+"="+v for k, v in d.items()])


def url2dict(u):
    url_parse = urlparse(u)
    if url_parse.netloc == '':
        params = url_parse.path
    else:
        params = url_parse.query if url_parse.query != '' else url_parse.fragment
    return {k: v[0] if len(v) == 1 else v for k, v in parse_qs(params).items()}

if __name__ == '__main__':
    print url2dict("https://openapi.baidu.com/oauth/2.0/login_success#expires_in=2592000&access_token=23.2123f44b3f36068e93d5081292a641bc.2592000.1503392341.2115468124-9921852&session_secret=73080d3dab9b7cc0b31cd09747587143&session_key=9mtqV9wazuil2n9Z0MGSvdHSOQtCoQ612yhNEaVxRC9nSej24rSEwsdrlgQntug3jlNrfpOapIbClFyKQso%2BGZurai%2FTLF7eKw%3D%3D&scope=basic+netdisk")
    print url2dict("https://openapi.baidu.com/oauth/2.0/login_success?expires_in=2592000&access_token=23.2123f44b3f36068e93d5081292a641bc.2592000.1503392341.2115468124-9921852&session_secret=73080d3dab9b7cc0b31cd09747587143&session_key=9mtqV9wazuil2n9Z0MGSvdHSOQtCoQ612yhNEaVxRC9nSej24rSEwsdrlgQntug3jlNrfpOapIbClFyKQso%2BGZurai%2FTLF7eKw%3D%3D&scope=basic+netdisk")
    print url2dict("expires_in=2592000&access_token=23.2123f44b3f36068e93d5081292a641bc.2592000.1503392341.2115468124-9921852&session_secret=73080d3dab9b7cc0b31cd09747587143&session_key=9mtqV9wazuil2n9Z0MGSvdHSOQtCoQ612yhNEaVxRC9nSej24rSEwsdrlgQntug3jlNrfpOapIbClFyKQso%2BGZurai%2FTLF7eKw%3D%3D&scope=basic+netdisk")
