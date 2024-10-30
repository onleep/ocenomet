from database import DB, model_classes
from tools import proxyDict, headers, recjson, logging
from validate_page import validatePage
import requests
import random
import time


def getResponse(page=None, type=0, respTry=5, sort=None, rooms=None) -> None | str:
    URL = 'https://www.cian.ru'
    # respTry = respTry if respTry is not None else len(proxyDict)

    mintime = sorted(proxyDict.values())[1]
    if (mintime > (timenow := time.time())):
        logging.info(f'No available proxies, waiting {(mintime - timenow):.2f} seconds')
        time.sleep(max(0, mintime - timenow))

    proxy = random.choice([k for k, v in proxyDict.items() if v <= time.time()])
    if type:
        try:
            start = time.time()
            response = requests.get(f'{URL}/sale/flat/{page}/', headers=random.choice(headers),
                                proxies={'http': proxy, 'https': proxy}, timeout=10)
            spendtime = time.time() - start
            logging.info(f'Requests time {proxy} = {spendtime:.2f}')
        except Exception as e:
            proxyDict[proxy] = time.time() + (1 * 60)
            logging.error(f'Proxy {proxy}: {e}')
            return getResponse(page, type, respTry - 1)
    else:
        params = {'deal_type': 'sale',
                  'offer_type': 'flat',
                  'p': page,
                  'region': 1,
                  }
        if rooms: params.update({rooms: 1})
        if sort: params.update({'sort': sort})
        try:
            start = time.time()
            response = requests.get(f'{URL}/cat.php', params=params, headers=random.choice(headers),
                                proxies={'http': proxy, 'https': proxy}, timeout=10)
            spendtime = time.time() - start
            logging.info(f'Requests time {proxy} = {spendtime:.2f}')
        except Exception as e:
            proxyDict[proxy] = time.time() + (1 * 60)
            logging.error(f'Proxy {proxy}: {e}')
            return getResponse(page, type, respTry - 1)
        
    rcode = response.status_code
    if rcode != 200:
        logging.error(f"GetResponse Page {page} | Retry: {respTry} | {rcode}")
        if not respTry: return None
        if rcode in (403, 429): proxyDict[proxy] = time.time() + (2 * 60)
        else: proxyDict[proxy] = time.time() + (1 * 60)
        return getResponse(page, type, respTry - 1)
    proxyDict[proxy] = time.time() + 5
    return response.text


def prePage(data=None, type=0) -> dict:
    key = '"offerData":' if type else '"pageview",'
    if pageJS := recjson(rf'{key}\s*(\{{.*?\}})', data):
        return pageJS
    return {}


def listPages(page=None, sort=None, rooms=None) -> str | list:
    pagesList=[]
    if not (response := getResponse(page, type=0, sort=sort, rooms=rooms)):
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


def apartPage(pagesList=None) -> None | str | list:
    pages_cnt = 0
    for page in pagesList:
        if DB.select(model_classes['offers'], filter_conditions={'cian_id': page}):
            logging.info(f"Apart page {page} already exists") 
            continue
            # return 'END'
        if not (response := getResponse(page, type=1)):
            continue
        pageJS = prePage(response, type=1)
        if data := validatePage(pageJS):
            instances = [model(**data[key]) for key, model in model_classes.items() if key in data]
            logging.info(f"Apart page {page} is adding")
            DB.insert(*instances)
            pages_cnt += 1
        continue
    logging.info(f"Apart pages {pagesList} is END")
    if not pages_cnt: return
    return 'OK'


def main(page=1, errors=0):
    while errors < 30:
        for rooms in ['', 'room1', 'room2', 'room3']:
            for sort in ['', 'creation_date_asc', 'creation_date_desc']:
                pglist = listPages(page, sort, rooms)
                if pglist == 'END': continue
                data = apartPage(pglist)
                if data == 'END': continue
                if not data: 
                    logging.info(f"Error parse count: {errors}")
                    errors += 1
                else: errors = 0
                logging.info(f"Page: {page}\nRooms: {rooms}\nSort: {sort}\nEND")
                page += 1
        return 'OK'
    logging.info(f"Error limit {errors} reached")
    return 'Error limit reached'


if __name__ == "__main__":
    print(main())
