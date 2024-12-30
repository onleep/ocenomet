import requests
import pandas as pd
import json

def get_data_page(url):
    """Получает данные с объявления Циан"""
    endpoint = "http://62.113.119.220:8000/getparams"
    try:
        response = requests.get(endpoint, params={"url": url}, timeout=120)
        response.raise_for_status()
        data = response.json()
        
        if "error" in data:
            return f"Ошибка: {data['error']}"
        if not data:
            return "Ошибка: Получены пустые данные."
        
        if isinstance(data, str):
            data = json.loads(data)

        df = pd.json_normalize(data).replace({None: pd.NA})

        return df
    except requests.exceptions.RequestException as e:
        return f"Произошла ошибка при запросе: {e}"

def get_predict_price(input_data):
    """Получает предсказанную цену от модели"""
    endpoint = "http://62.113.119.220:8000/predict"
    try:
        response = requests.get('http://62.113.119.220:8000/predict', json={'hello': 121})
        response.raise_for_status()
        data = response.json()

        if "price" in data:
            return float(data["price"])
        elif "error" in data:
            return f"Ошибка: {data['error']}"
        else:
            return "Ошибка: Неизвестный ответ от сервера."
    except requests.exceptions.RequestException as e:
        return f"Произошла ошибка при запросе: {e}"


