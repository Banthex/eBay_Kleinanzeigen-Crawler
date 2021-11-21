import requests
from Proxy import get_proxy
import time
from bs4 import BeautifulSoup
import json
import os
from Item import item
from Cache import cache
import Logger

class monitoring:
    
    __ENCODING = 'utf8'
    __BASE_URL = 'https://www.ebay-kleinanzeigen.de'
    __HEADER = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
                ,'accept-encoding': 'gzip, deflate, br'
                ,'accept-language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7'}
    
    def __init__(self,parser_args) -> None:
        self.url = parser_args.url
        self.output_json = parser_args.output_json
        self.file_name = parser_args.file_name
        self.output_folder = parser_args.output_folder
        self.proxy = parser_args.proxy
        self.sleep = parser_args.sleep
        Logger.level = parser_args.log_level
        Logger.date_format = parser_args.log_date_format
        self._cache_size = parser_args.cache
        self._cache = cache(self._cache_size)
        self._saved_hash = list()
        self.start_monitoring()

    def __response(self,) -> requests.Response:
        if self.proxy:
            proxy = get_proxy()
            res = requests.get(url=self.url, headers=self.__HEADER, proxies={'http://':'http://'+proxy, 'https://':'https://'+proxy}, allow_redirects=True)
        else:
            res = requests.get(url=self.url, headers=self.__HEADER)
        res.encoding = self.__ENCODING
        return res

    def __hash_items(self, items:list) -> int:
        return hash(tuple(items))

    def __call_succesfull(self, response:requests.Response) -> bool:
        return response.status_code < 400 and str(response.content).startswith("b'<!DOCTYPE html>")

    def __parse_content(self, response:requests.Response) -> list:
        soup = BeautifulSoup()
        try:
            soup = BeautifulSoup(response.text, 'html.parser')
        except AttributeError as e:
            print(e, 'Response: ',response)
        items = soup.find_all('article', attrs= {'class': 'aditem'})
        aditem:item = None
        aditems = list()
        for i in items:
            sponsored = i.find('i', attrs={'class','icon icon-smaller icon-feature-topad'})
            if sponsored:
                continue  
            id = i.get('data-adid')
            if id:
                aditem = item(id)
                link = i.get('data-href')
                
                if link:
                    aditem.set_link(self.__BASE_URL + link)
                name = i.find('a', attrs= {'class': 'ellipsis'})
               
                if name:
                    aditem.set_name(name.get_text().strip().replace('\n',' '))                
                desc = i.find('p', attrs= {'class': 'aditem-main--middle--description'})
                
                if desc:
                    aditem.set_desc(desc.get_text().strip().replace('\n',' '))

                price = i.find('p', attrs= {'class': 'aditem-main--middle--price'})
                if price:
                    aditem.set_price(price.get_text().strip().replace('\n',' '))
                
                date = i.find('div', attrs= {'class': 'aditem-main--top--right'})
                if date:
                    aditem.set_date(date.get_text().strip().replace('\n',' '))
                
                address = i.find('div', attrs= {'class': 'aditem-main--top--left'})
                if address:
                    aditem.set_address(address.get_text().strip().replace('\n',' '))
                
                tags = i.find_all('span', attrs= {'class': 'simpletag tag-small'})
                if tags:
                    tag_dict = dict()
                    for t in range(len(tags)):
                        tag_dict['Tag_'+str(t)] = tags[t].get_text().strip().replace('\n',' ')
                    aditem.set_tags(tag_dict)
                aditems.append(aditem)  
        return aditems

    def __dump_content(self):
        file = self.file_name + '.json'
        if not os.path.isdir(self.output_folder):
            os.mkdir(self.output_folder)
        with open(file=self.output_folder + file, mode='wb') as f:
            f.write(json.dumps(self._cache.to_dict(), indent=4, ensure_ascii=False).encode(self.__ENCODING))


    def _analyse_response(self,response:requests.Response):
        ad_items = self.__parse_content(response)
        new_hash = self.__hash_items(ad_items)
        if not new_hash == self._saved_hash:
            for i in ad_items:
                l_item = self._cache.isin(i)
                if l_item == None:
                    self._cache.add(i)
                    Logger.added(str(i))
                elif l_item.get_price() != i.get_price() :
                    self._cache.replace(l_item, i)
                    Logger.changed(str(i))
            if self.output_json:
                self.__dump_content()
        else:
            Logger.info('No changes!')
        self._saved_hash = new_hash
    
    def __monitoring(self):
        while True:
            res = self.__response()
            if self.__call_succesfull(res):
                self._analyse_response(res)         
            else:
                Logger.error('Bad response')
            time.sleep(self.sleep)

    def start_monitoring(self):
        self.__monitoring()

