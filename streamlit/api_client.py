import httpx
import numpy as np
import json
import streamlit as st

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

def prepare_data(X, y):
    """Преобразует данные X и y в ожидаемый формат"""
    X_prepared = [
        {f"feature_{i+1}": float(value) for i, value in enumerate(row)}
        for row in X
    ]
    
    y_prepared = [float(value) for value in y]
    
    return X_prepared, y_prepared



def fit_model(model_id, model_type, hyperparameters, X, y):
    """Создает и обучает модель"""
    endpoint = "http://62.113.119.220:8000/api/fit"

    config = {
        "id": model_id,
        "ml_model_type": model_type,
        "hyperparameters": hyperparameters
    }
    
    X_prepared, y_prepared = prepare_data(X, y)
    print("Prepared X:", X_prepared)
    print("Prepared y:", y_prepared)

    payload = [
        {
            "X": X_prepared,
            "y": y_prepared,
            "config": config
        }
    ]
    print("Payload sent to server:")
    print(json.dumps(payload, indent=2))

    try:
        response = httpx.post(endpoint, json=payload, timeout=300)
        print("Response status code:", response.status_code)
        print("Response text:", response.text)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        st.error(f"Сервер вернул ошибку: {e.response.status_code}")
        st.error(f"Детали ошибки: {e.response.text}")
        return f"Ошибка при обучении модели: {e.response.status_code}"
    except Exception as e:
        st.error(f"Неизвестная ошибка: {e}")
        return f"Ошибка: {e}"



def list_models():
    """Получает список всех моделей"""
    endpoint = "http://62.113.119.220:8000/api/list_models"
    try:
        response = httpx.get(endpoint, timeout=60)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return f"Ошибка при получении списка моделей: {e}"


def load_model(model_id):
    """Загружает модель"""
    endpoint = "http://62.113.119.220:8000/api/load"
    try:
        response = httpx.post(endpoint, json={"id": model_id}, timeout=60)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return f"Ошибка при загрузке модели: {e}"


def unload_model():
    """Выгружает все модели"""
    endpoint = "http://62.113.119.220:8000/api/unload"
    try:
        response = httpx.post(endpoint, timeout=60)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return f"Ошибка при выгрузке моделей: {e}"


def remove_model(model_id):
    """Удаляет модель"""
    endpoint = f"http://62.113.119.220:8000/api/remove/{model_id}"
    try:
        response = httpx.delete(endpoint, timeout=60)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return f"Ошибка при удалении модели: {e}"


def remove_all_models():
    """Удаляет все модели"""
    endpoint = "http://62.113.119.220:8000/api/remove_all"
    try:
        response = httpx.delete(endpoint, timeout=60)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return f"Ошибка при удалении всех моделей: {e}"
