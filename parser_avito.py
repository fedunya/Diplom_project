import os
import json
from urllib.parse import unquote
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from db_func import check_dbase, create_dbase, record_dbase
from bot_func import format_text, send_message
from csv_func import add_data, create_csv

__all__ = ['parser_avito', 'get_json', 'get_info', 'get_offer', 'record_data']

AVITO = 'https://www.avito.ru'
url = 'https://www.avito.ru/rostov-na-donu/kvartiry/prodam-ASgBAgICAUSSA8YQ?context=H4sIAAAAAAAA_0q0MrSqLraysFJKK8rPDUhMT1WyLrYyt1JKTixJzMlPV7KuBQQAAP__dhSE3CMAAAA&f=ASgBAgICAkSSA8YQkL4Nlq41'

def parser_avito(url):
    current_directory = os.getcwd()
    option = webdriver.ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-logging'])
    service = webdriver.ChromeService(executable_path=current_directory + '/chromedriver.exe')
    browser = webdriver.Chrome(service=service, options=option)
    browser.get(url)
    index_page = browser.page_source
    browser.quit()
    return index_page

def get_json(index_page):
    soup = BeautifulSoup(index_page, 'lxml')
    scripts = soup.find_all('script')
    for script in scripts:
        if 'window.__initialData__' in script.text:
            _ = script.text.split(';')[0].split('=')[-1].strip()[1:-1]
            _ = unquote(_)
            data_json = json.loads(_)
            for key in data_json:
                if 'single-page' in key:
                    catalog = data_json[key]['data']['catalog']['items']
            break
    return catalog

def get_offer(item):
    offer = {}
    offer['offer_id'] = item['id']
    offer['url'] = AVITO + item['urlPath']
    offer['adress'] = item['location']['name'] + ', ' + item['geo']['formattedAddress']
    offer['price'] = item['priceDetailed']['value']
    date_time = datetime.fromtimestamp(int(item['sortTimeStamp'] / 1000))
    offer['datetime'] = datetime.strftime(date_time, '%d %B %Y %H:%M')
    offer['date_time'] = date_time
    offer['title'] = item['title'].replace('\xa0', ' ')
    if len(item['geo']['geoReferences']) != 0:
        offer['district'] = item['geo']['geoReferences'][0]['content']
    else:
        offer['district'] = 'без района'
    return offer

def record_data(items):
    for item in items:
        if 'id' in item.keys():
            offer_id = item['id']
            if check_dbase(offer_id) is None:
                offer = get_offer(item)
                record_dbase(offer)
                square = add_data(offer)
                text = format_text(offer, square)
                send_message(text)
                

def main():
    current_directory = os.getcwd()
    if not os.path.exists(current_directory + '/realty_dataset.csv'):
        create_csv()
    if not os.path.exists(current_directory + '/realty.db'):
        create_dbase()
    index_page = parser_avito(url)
    items = get_json(index_page)
    record_data(items)


if __name__ == '__main__':
    main()

