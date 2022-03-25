import requests
from bs4 import BeautifulSoup
from Item import item
import html


__BASE_URL_IMMOSCOUT = 'https://www.immobilienscout24.de'

def analyze(response:requests.Response):
    soup = BeautifulSoup()
    try:
        soup = BeautifulSoup(html.unescape(response.text), 'html.parser')
    except AttributeError as e:
            print(e, 'Response: ',response)
            return
    

def __immoscout(soup: BeautifulSoup):
    items = soup.find_all('article', attrs= {'class': 'result-list__listing '})
    aditem:item = None
    aditems:list = list()
    for i in items:
        id = i.get('data-id')
        if id:
            aditem = item(id)
            
            link = i.find('a', attrs= {'class': 'slick-slide slick-cloned'})
            if link:
                aditem.set_link(__BASE_URL_IMMOSCOUT + link.get('href').strip())

            name = i.find('h5', attrs= {'class': 'result-list-entry__brand-title font-h6 onlyLarge font-ellipsis font-regular nine-tenths'})
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
                address = address.get_text().strip().replace('\n',' ')
                address = re.sub('\s{2,}',' ',address)
                aditem.set_address(address)
            
            tags = i.find_all('span', attrs= {'class': 'result-list-entry__secondary-criteria'})
            if tags:
                tag_dict = dict()
                for t in range(len(tags)):
                    tag_dict['Tag_'+str(t)] = tags[t].get_text().strip().replace('\n',' ')
                aditem.set_tags(tag_dict)
            aditems.append(aditem) 
    return aditems[::-1]