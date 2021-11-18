import hashlib
import requests
from Proxy import get_proxy
import time
from datetime import datetime
from bs4 import BeautifulSoup
import json
from deepdiff import DeepDiff


class montioring:
    __HEADER = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}
    __DUMP_FOLDER = 'dump/'
    __ENCODING = 'utf8'
    __BASE_URL = 'https://www.ebay-kleinanzeigen.de'

    def __init__(self,parser_args) -> None:
        self.url = parser_args.url
        self.json_dump = parser_args.json_dump
        self.proxy = parser_args.proxy
        self.sleep = parser_args.sleep
        self.saved_response = ''
        self.start_monitoring()

    def __response(self,) -> requests.Response:
        if self.proxy:
            proxy = get_proxy()
            res = requests.get(url=self.url, headers=self.__HEADER, proxies={'http://':proxy, 'https://':proxy})
        else:
            res = requests.get(url=self.url, headers=self.__HEADER)
        res.encoding = self.__ENCODING
        return res

    def __call_succesfull(self, response:requests.Response) -> bool:
        return response.status_code == 200 and str(response.content).startswith("b'<!DOCTYPE html>")

    def __hash_response(self, response:requests.Response) -> str:
        return hashlib.sha256(self.__parse_content(response).encode(self.__ENCODING)).hexdigest()

    def __init_hash(self):
        global __response_saved
        for i in range(5):
            response = self.__response()
            if(self.__call_succesfull(response)):
                if self.json_dump:
                    self.__dump_content(response)
                self.saved_response = response
                return self.__hash_response(response)
        return False, response

    def __parse_content(self, response:requests.Response):
        soup = BeautifulSoup(response.content, 'html.parser')
        items = soup.find_all('article', attrs= {'class': 'aditem'})
        results = {}
        for i in items:
            result= {}
            id = i.get('data-adid')
            if id:
                result['Article_id'] = id
            link = i.get('data-href')
            if link:
                result['Article_link'] = self.__BASE_URL + link
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
            
            results['aditem_'+id] = result

        return json.dumps(results, sort_keys=True, indent=4, ensure_ascii=False)

    def __dump_content(self, response:requests.Response):
        file = datetime.now().strftime('%H_%M_%S_%d_%m_%Y') + '.json'
        with open(file=self.__DUMP_FOLDER + file, mode='w', encoding=self.__ENCODING) as f:
            f.write(self.__parse_content(response))
        

    def __monitoring(self, init_hash):
        while True:
            time.sleep(self.sleep)
            try:
                res = self.__response()
                if self.__call_succesfull(res):
                    new_hash = self.__hash_response(res)
                    if new_hash == init_hash:
                        print("No change!")
                        continue
                    else:
                        init_hash = new_hash
                        print(DeepDiff(self.__parse_content(self.saved_response), self.__parse_content(res)), ignore_order=True, verbose_level=1, view='tree')
                        self.saved_response = res
                        if self.json_dump:
                            self.__dump_content(res)
                        print("Website changed!")
            except Exception as e:
                print(e)

    def start_monitoring(self):
        init_hash = self.__init_hash()
        if not init_hash:
            print('Monitoring failed! Url:', self.url)
            return False
        self.__monitoring(init_hash)

