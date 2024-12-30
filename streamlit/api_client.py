import httpx
import pandas as pd

def get_data_page(url):
    """Получает данные с объявления Циан"""
    endpoint = "http://62.113.119.220:8000/api/getparams"
    try:
        response = httpx.get(endpoint, params={'url': url}, timeout=120)
        response.raise_for_status()
        return response
    except Exception as e:
        return f"Произошла ошибка при запросе: {e}", None

def get_predict_price(input_data):
    """Получает предсказанную цену от модели"""
    endpoint = "http://62.113.119.220:8000/api/predict"
    try:
        response = httpx.post(endpoint, json={'data': input_data})
        response.raise_for_status() 
        data = response.json()

        return float(data["price"])
    except Exception as e:
        return f"Ошибка: {e}"
