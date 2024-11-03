import re
import json
import logging
import os


def recjson(regex, data, ident=None) -> None | dict:
    match = re.search(regex, data)
    if not match:
        logging.error(f"Recjson not match")
        return

    start_idx = match.start(1)
    end_idx, open_brackets = start_idx + 1, 1

    while open_brackets > 0 and end_idx < len(data):
        open_brackets += 1 if data[end_idx] == '{'\
            else - 1 if data[end_idx] == '}' else 0
        end_idx += 1
    if ident:
        json_str = f'{{"{ident}": {data[start_idx:end_idx]}}}'
    else:
        json_str = data[start_idx:end_idx]

    try:
        fdata = json.loads(json_str)
        return fdata
    except Exception as ex:
        logging.error(f"Recjson error:\n{ex}")
        return


logging.basicConfig(format='%(asctime)s | %(levelname)s: %(message)s',
                    datefmt="%Y-%m-%d %H:%M:%S", level=logging.INFO, filename="ocenomet.log", filemode="a")

proxyDict = {proxy: 0.0 for proxy in (os.getenv(f'PROXY{i}') for i in range(1, 14)) if proxy}
proxyDict[''] = 0.0

headers = [
    {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.90 Safari/537.36'},
    {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1_0) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.2 Safari/605.1.15'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Gecko/20100101 Firefox/118.0'},
    {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:118.0) Gecko/20100101 Firefox/118.0'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; Trident/7.0; AS; rv:11.0) like Gecko'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.90 Safari/537.36'}
]
