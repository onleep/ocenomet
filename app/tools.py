import re
import json
import logging


def recjson(regex: str, data, ident=None) -> None | dict:
    match = re.search(regex, data)
    if not match:
        logging.error(f"Recjson not match")
        return None

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
        # with open('parsepages.json', 'w') as file:
        #     json.dump(fdata, file, ensure_ascii=False, indent=4)
        return fdata
    except Exception as ex:
        logging.error(f"Recjson error:\n{ex}")
        return None


logging.basicConfig(format='%(asctime)s | %(levelname)s: %(message)s',
                    datefmt="%Y-%m-%d %H:%M:%S", level=logging.INFO, filename="ocenomet.log", filemode="a")

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'}
