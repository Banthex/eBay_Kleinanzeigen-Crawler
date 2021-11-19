import hashlib
import requests
from Proxy import get_proxy
import time
from datetime import datetime
from bs4 import BeautifulSoup
import json
from deepdiff import DeepDiff
import re
import os

class monitoring:
    
    __ENCODING = 'utf8'
    __BASE_URL = 'https://www.ebay-kleinanzeigen.de'
    
    def __init__(self,parser_args) -> None:
        self.url = parser_args.url
        self.output_json = parser_args.output_json
        self.json_pref = parser_args.json_pref
        self.output_folder = parser_args.output_folder
        self.proxy = parser_args.proxy
        self.sleep = parser_args.sleep
        self._saved_response = 'Init response - Empty'
        self._current_hash = '0x01'
        self._header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}
        self.start_monitoring()

    def __response(self,) -> requests.Response:
        if self.proxy:
            proxy = get_proxy()
            res = requests.get(url=self.url, headers=self._header, proxies={'http://':'http://'+proxy, 'https://':'https://'+proxy}, allow_redirects=True)
        else:
            res = requests.get(url=self.url, headers=self._header)
        res.encoding = self.__ENCODING
        return res

    def __call_succesfull(self, response:requests.Response) -> bool:
        return response.status_code < 400 and str(response.content).startswith("b'<!DOCTYPE html>")

    def __hash_response(self, response:requests.Response) -> str:
        return hashlib.sha256(json.dumps(self.__parse_content(response)).encode(self.__ENCODING)).hexdigest()

    def __parse_content(self, response:requests.Response) -> dict:
        results = dict()
        soup = BeautifulSoup()
        try:
            soup = BeautifulSoup(response.content, 'html.parser')
        except AttributeError as e:
            print(e, 'Response: ',response)
            return results
        items = soup.find_all('article', attrs= {'class': 'aditem'})
        for i in items:
            result= {}
            sponsored = i.find('i', attrs={'class','icon icon-smaller icon-feature-topad'})
            if sponsored:
                continue
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
            
            tags = i.find_all('span', attrs= {'class': 'simpletag tag-small'})
            if tags:
                for t in range(len(tags)):
                    result['Tag_'+str(t)] = tags[t].get_text().strip().replace('\n',' ')
                #result['Article_shipping'] = shipping.get_text().strip().replace('\n',' ')
            
            results['aditem_'+id] = result

        return results

    def __dump_content(self, response:requests.Response):
        file = self.json_pref + '_' + datetime.now().strftime('%H_%M_%S_%d_%m_%Y') + '.json'
        if not os.path.isdir(self.output_folder):
            os.mkdir(self.output_folder)
        with open(file=self.output_folder + file, mode='w', encoding=self.__ENCODING) as f:
            f.write(json.dumps(self.__parse_content(response), sort_keys=True, indent=4, ensure_ascii=False))


    def _analyse_response(self,response:requests.Response):
        new_hash = self.__hash_response(response)
        if new_hash == self._current_hash:
            print("No change!")
        else:
            new_dict = self.__parse_content(response)
            diff = DeepDiff(self.__parse_content(self._saved_response),new_dict,ignore_order=True)
            try:
                for dif in re.findall("aditem_\d+",str(diff['dictionary_item_added'])):
                    print('Added: ' + new_dict[str(dif)]['Article_link'])
                    print(new_dict[str(dif)]['Article_price'])
                for dif in re.findall("aditem_\d+",str(diff['values_changed'])):
                    print('Changed: ' + new_dict[str(dif)]['Article_link'])
                    print(new_dict[str(dif)]['Article_price'])
            except KeyError as e:
                pass
            self._current_hash = new_hash
            self._saved_response = response
        if self.output_json:
            self.__dump_content(response)
    
    def __monitoring(self):
        while True:
            res = self.__response()
            if self.__call_succesfull(res):
                self._analyse_response(res)         
            else:
                print('Bad Response')
            time.sleep(self.sleep)

    def start_monitoring(self):
        self.__monitoring()

