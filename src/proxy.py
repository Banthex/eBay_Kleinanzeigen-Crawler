from lxml.html import fromstring
import requests
from itertools import cycle
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

def _proxy_test(proxy):
    return requests.get('https://www.google.com/', headers=_HEADER, proxies={'http://':'http://'+proxy, 'https://':'https://'+proxy}).status_code < 400

def get_proxy():
    while True:
        proxies = __parse_proxies()
        if len(proxies) >0:
            proxy = proxies[randint(0, len(proxies)-1)]
            if _proxy_test(proxy):
                return proxy
            else:
                print('Proxy not working') 