import hashlib
import requests
from proxy import get_proxy
import time
from datetime import datetime
from bs4 import BeautifulSoup
import json



__HEADER = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}
__DUMP_FOLDER = 'dump/'
__ENCODING = 'utf8'

def __response(url:str):
    proxy = get_proxy()
    res = requests.get(url=url, headers=__HEADER, proxies={'http://':proxy, 'https://':proxy})
    res.encoding = __ENCODING
    return res

def __call_succesfull(response:requests.Response):
    return response.status_code == 200 and str(response.content).startswith("b'<!DOCTYPE html>")

def __hash_response(response:requests.Response):
    return hashlib.sha256(__parse_content(response).encode(__ENCODING)).hexdigest()

def __init_hash(url:str):
    for i in range(20):
        response = __response(url)
        if(__call_succesfull(response)):
            __dump_content(response)
            return __hash_response(response)
        time.sleep(1)
    return False

def __parse_content(response:requests.Response):
    soup = BeautifulSoup(response.content, 'html.parser')
    items = soup.find_all('article', attrs= {'class': 'aditem'})
    results = {}
    for i in items:
        result= {}
        id = i.get('data-adid')
        name = i.find('a', attrs= {'class': 'ellipsis'})
        if name:
            result['Article_name'] = name.get_text().strip().replace('\n',' ')
        
        desc = i.find('p', attrs= {'class': 'aditem-main--middle--description'})
        if desc:
            result['Article_desc'] = desc.get_text().strip().replace('\n',' ')
        
        price = i.find('p', attrs= {'class': 'aditem-main--middle--price'})
        if price:
           result['Article_price'] = price.get_text().strip().replace('\n',' ')
        
        date = i.find('div', attrs= {'class': 'aditem-main--top--right'})
        if date:
            result['Article_date'] = date.get_text().strip().replace('\n',' ')
        
        address = i.find('div', attrs= {'class': 'aditem-main--top--left'})
        if address:
            result['Article_adress'] = address.get_text().strip().replace('\n',' ')
        
        shipping = i.find('span', attrs= {'class': 'simpletag tag-small'})
        if shipping:
            result['Article_shipping'] = shipping.get_text().strip().replace('\n',' ')
        
        results[str(id)] = result

    return json.dumps(results, sort_keys=True, indent=4, ensure_ascii=False)

def __dump_content(response:requests.Response):
    file = datetime.now().strftime('%H_%M_%S_%d_%m_%Y') + '.json'
    with open(file=__DUMP_FOLDER + file, mode='w', encoding=__ENCODING) as f:
        f.write(__parse_content(response))
    

def __monitoring(init_hash, url):
    while True:
        time.sleep(15)
        try:
            res = __response(url)
            if __call_succesfull(res):
                new_hash = __hash_response(res)
                if new_hash == init_hash:
                    print("No change!")
                    continue
                else:
                    init_hash = new_hash
                    __dump_content(res)
                    print("Website changed!")
        except Exception as e:
            print(e)

def start_monitoring(url:str):
    init_hash = __init_hash(url)
    if not init_hash:
        print('Monitoring failed! Url:', url)
        return False
    __monitoring(init_hash, url)

