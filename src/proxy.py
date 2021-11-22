from lxml.html import fromstring
import requests
from random import randint

_HEADER = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}

def __parse_proxies():
    url = 'https://free-proxy-list.net/'
    response = requests.get(url, headers=_HEADER)
    parser = fromstring(response.text)
    proxies = list()
    for i in parser.xpath('//tbody/tr')[:100]:
        if i.xpath('.//td[7][contains(text(),"yes")]') and i.xpath('.//td[5][contains(text(),"elite proxy")]'):
            proxy = ":".join([i.xpath('.//td[1]/text()')[0].strip(), i.xpath('.//td[2]/text()')[0].strip()])
            proxies.append(proxy)
    return proxies

def _proxy_test(proxies):
    with requests.get('http://www.google.com', proxies=proxies, timeout=0.5, stream=True) as r:
            if r.raw.connection.sock:
                if r.raw.connection.sock.getpeername()[0] == proxies['https'].split(':')[1][2:]:
                    return proxies

def get_proxy():
    while True:
        proxies = __parse_proxies()
        if len(proxies) >0:
            proxy = proxies[randint(0, len(proxies)-1)]
            proxies={'http':'http://'+proxy, 'https':'https://'+proxy}
            if _proxy_test(proxies):
                return proxies
            else:
                print('Proxy not working') 