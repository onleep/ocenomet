from database import DB, model_classes
from tools import headers, recjson, logging
from validate_page import validatePage
import requests
import random
import time


def getResponse(page, type=0, respTry=3) -> None | str:
    URL = 'https://www.cian.ru'
    if type:
        response = requests.get(f'{URL}/sale/flat/{page}/', headers=headers)
    else:
        params = {'deal_type': 'sale',
                  'offer_type': 'flat',
                  'p': page,
                  'region': 1,
                  'sort': 'creation_date_asc'}
        response = requests.get(f'{URL}/cat.php', params=params, headers=headers)
    rcode = response.status_code
    if rcode != 200:
        logging.error(f"GetResponse Page {page} | Retry: {respTry} | {rcode}")
        if not respTry: return None
        if rcode in (403, 429): time.sleep(60 * 5)
        else: time.sleep(random.uniform(30, 60))
        return getResponse(page, type, respTry=respTry - 1)
    time.sleep(random.uniform(10, 30))
    return response.text


def prePage(data, type=0) -> dict:
    key = '"offerData":' if type else '"pageview",'
    if pageJS := recjson(rf'{key}\s*(\{{.*?\}})', data):
        return pageJS
    return {}


def listPages(page) -> str | list:
    pagesList=[]
    if not (response := getResponse(page, type=0)):
        return []
    pageJS = prePage(response, type=0)
    if pageJS.get('page', {}).get('pageNumber') != page:
        logging.info(f"Prewiew page {page} is END")
        return 'END'
    if products := pageJS.get('products'):
        for i in products:
            if id := i.get('cianId'):
                logging.info(f"Prewiew page {id} appended")
                pagesList.append(id)
        return pagesList
    logging.info(f"Prewiew page {page} is None")
    return []


def apartPage(pagesList) -> None | list:
    for page in pagesList:
        if DB.select(model_classes['offers'], filter_conditions={'cian_id': page}):
            logging.info(f"Apart page {page} already exists") 
            continue
        if not (response := getResponse(page, type=1)):
            return
        pageJS = prePage(response, type=1)
        if data := validatePage(pageJS):
            instances = [model(**data[key]) for key, model in model_classes.items() if key in data]
            logging.info(f"Apart page {page} is adding")
            DB.insert(*instances)
        # with open(f'{page}.json', 'w') as file:
        #     json.dump(data, file, ensure_ascii=False, indent=4)
        continue
    logging.info(f"Apart pages {pagesList} is END")


def main(page=1, errors=0):
    while errors < 30:
        pglist = listPages(page)
        if pglist == 'END': return 'END'
        data = apartPage(pglist)
        if not data: errors += 1
        else: errors = 0
        page += 1


if __name__ == "__main__":
    print(main())
