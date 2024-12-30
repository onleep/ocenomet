from .database import DB, model_classes, Offers
from .tools import proxyDict, headers, recjson, logging
from .validate_page import validatePage
import random
import httpx
import time


def getResponse(page, type=0, respTry=5, sort=None, rooms=None) -> None | str:
    URL = 'https://www.cian.ru'

    mintime = sorted(proxyDict.values())[2]
    if (mintime > (timenow := time.time())):
        logging.info(f'No available proxies, waiting {(mintime - timenow):.2f} seconds')
        time.sleep(max(0, mintime - timenow))

    proxy = random.choice([k for k, v in proxyDict.items() if v <= time.time()])

    url = f'{URL}/sale/flat/{page}/' if type else f'{URL}/cat.php'
    params = None if type else {
        'deal_type': 'sale',
        'offer_type': 'flat',
        'p': page,
        'region': 1,
        **({rooms: 1} if rooms else {}),
        **({'sort': sort} if sort else {}),
    }
    try:
        start = time.time()
        response = httpx.get(url, params=params, headers=random.choice(headers),
                                proxies={'http': proxy, 'https': proxy}, timeout=10)
        logging.info(f'Requests time {proxy} = {(time.time() - start):.2f}')
    except Exception as e:
        proxyDict[proxy] = time.time() + (1 * 60)
        logging.error(f'Proxy {proxy}: {e}')
        return getResponse(page, type, respTry - 1)

    rcode = response.status_code
    if rcode != 200:
        logging.error(f"GetResponse Page {page} | Retry: {respTry} | {rcode}")
        if not respTry: return
        if rcode in (403, 429): proxyDict[proxy] = time.time() + (3 * 60)
        elif rcode == 404: return
        else: proxyDict[proxy] = time.time() + (1 * 60)
        return getResponse(page, type, respTry - 1)
    proxyDict[proxy] = time.time() + 10
    return response.text


def prePage(data, type=0) -> dict:
    key = '"offerData":' if type else '"pageview",'
    if pageJS := recjson(rf'{key}\s*(\{{.*?\}})', data):
        return pageJS
    return {}


def listPages(page, sort=None, rooms=None) -> str | list:
    pagesList = []
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


def apartPage(pagesList, dbinsert=1) -> None | str | list | dict:
    pages_cnt = 0
    for page in pagesList:
        exist = False
        if dbinsert and DB.select(model_classes['offers'], filter_by={'cian_id': page}):
            exist = True
            logging.info(f"Apart page {page} already exists")
            continue # skip
        if not (response := getResponse(page, type=1)):
            continue
        pageJS = prePage(response, type=1)
        if data := validatePage(pageJS):
            if not dbinsert: return data
            if exist:
                instances = [(model, data[key])
                             for key, model in model_classes.items() if key in data]
                for model, update_values in instances:
                    logging.info(f"Apart page {page}, table {model} is updating")
                    DB.update(model, {'cian_id': page}, update_values)
            else:
                instances = [model(**data[key])
                             for key, model in model_classes.items() if key in data]
                logging.info(f"Apart page {page} is adding")
                DB.insert(*instances)
            pages_cnt += 1
        continue
    logging.info(f"Apart pages {pagesList} is END")
    if not pages_cnt: return
    return 'OK'


def main(npage=1, errors=0):
    for rooms in ['', 'room1', 'room2', 'room3', 'room4', 'room5', 'room6', 'room7', 'room8', 'room9']:
        for sort in ['', 'creation_date_asc', 'creation_date_desc']:
            page = npage
            errors = 0
            while errors < 30:
                pglist = listPages(page, sort, rooms)
                if pglist == 'END': 
                    logging.info('End of pglist reached')
                    break
                data = apartPage(pglist)
                if data == 'END': 
                    logging.info("End of data reached")
                    break
                if not data: 
                    errors += 1
                    logging.info(f'Error parse count: {errors}')
                    if errors >= 30:
                        logging.info(f'Error limit {errors} reached')
                        break
                else: errors = 0
                page += 1
            logging.info(f"Page: {page}\nRooms: {rooms}\nSort: {sort}\nEND")
    return 'OK'


if __name__ == "__main__":
    print(main())
