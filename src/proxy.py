from lxml.html import fromstring
import requests
from itertools import cycle
from random import randint

def __parse_proxies():
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = list()
    for i in parser.xpath('//tbody/tr')[:100]:
        if i.xpath('.//td[7][contains(text(),"yes")]') and i.xpath('.//td[5][contains(text(),"elite proxy")]'):
            proxy = ":".join([i.xpath('.//td[1]/text()')[0].strip(), i.xpath('.//td[2]/text()')[0].strip()])
            proxies.append(proxy)
    return proxies

def get_proxy():
    proxies = __parse_proxies()
    if len(proxies) >0:
        proxy_num = randint(0, len(proxies)-1)
    else:
        get_proxy()
    prox = proxies[proxy_num]
    return prox