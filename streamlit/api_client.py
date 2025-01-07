import httpx
import json
import streamlit as st
import httpx
import pandas as pd
from logger_setup import setup_logger
from mapping_utils import reorder_columns, map_dataframe

API_BASE_URL = st.secrets["API_BASE_URL"]
logger = setup_logger()

# Получение данных с объявления Циан
def get_data_page(url):
    """Получает данные с объявления Циан"""
    endpoint = f"{API_BASE_URL}/api/getparams"
    try:
        response = httpx.get(endpoint, params={'url': url}, timeout=120)
        response.raise_for_status()
        return response
    except Exception as e:
        return f"Произошла ошибка при запросе: {e}", None

# Получение предсказанной стоимости от модели
def get_predict_price(input_data):
    """Получает предсказанную цену от модели"""
    endpoint = f"{API_BASE_URL}/api/predict"
    try:
        response = httpx.post(endpoint, json={'data': input_data})
        response.raise_for_status()
        data = response.json()

        return float(data["price"])
    except Exception as e:
        return f"Ошибка: {e}"

# Подготовка данных для отправки на сервер
def prepare_data(X, y):
    """Преобразует данные X и y в ожидаемый формат"""
    X_prepared = [
        {f"feature_{i+1}": float(value) for i, value in enumerate(row)}
        for row in X
    ]
    
    y_prepared = [float(value) for value in y]
    
    return X_prepared, y_prepared

# Обучение модели
def fit_model(model_id, model_type, hyperparameters, X, y):
    """Создает и обучает модель"""
    endpoint = f"{API_BASE_URL}/api/fit"

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
        st.error(f"Детали ошибки: {e.response.text}")
        return f"Ошибка при обучении модели: {e.response.status_code}"
    except Exception as e:
        st.error(f"Неизвестная ошибка: {e}")
        return f"Ошибка: {e}"

# Получение списка всех моделей
def list_models():
    """
    Получает список всех моделей с подробной информацией.
    """
    endpoint = f"{API_BASE_URL}/api/list_models"
    try:
        response = httpx.get(endpoint, timeout=60)
        response.raise_for_status()
        models = response.json()
        print(models)
        return models
    except Exception as e:
        return f"Ошибка при получении списка моделей: {e}"

# Загрузка модели
def load_model(model_id):
    """Загружает модель"""
    endpoint = f"{API_BASE_URL}/api/load"
    try:
        response = httpx.post(endpoint, json={"id": model_id}, timeout=60)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return f"Ошибка при загрузке модели: {e}"

# Выгрузка всех моделей
def unload_model():
    """Выгружает все модели"""
    endpoint = f"{API_BASE_URL}/api/unload"
    try:
        response = httpx.post(endpoint, timeout=60)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return f"Ошибка при выгрузке моделей: {e}"

# Удаление конкретной модели
def remove_model(model_id):
    """Удаляет модель"""
    endpoint = f"{API_BASE_URL}/api/remove/{model_id}"
    try:
        response = httpx.delete(endpoint, timeout=60)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return f"Ошибка при удалении модели: {e}"

# Удаление всех моделей
def remove_all_models():
    """Удаляет все модели"""
    endpoint = f"{API_BASE_URL}/api/remove_all"
    try:
        response = httpx.delete(endpoint, timeout=60)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return f"Ошибка при удалении всех моделей: {e}"

# Получение данных с CIAN
@st.cache_data
def fetch_data(cian_url):
    try:
        logger.info(f"Получение данных с CIAN по ссылке: {cian_url}")
        response = get_data_page(cian_url)
        data = response.json()
        return data
    except Exception as e:
        logger.error(f"Ошибка при получении данных с CIAN: {e}")
        st.error(f"Ошибка: {e}")
        return None

# Получение реальной и предсказанной стоимости
def get_real_and_predicted_prices(result, data):
    result = map_dataframe(result, direction="to_english")
    result_cleaned = result.dropna(axis=1)
    real_price = float(result['price'].iloc[0])
    features = result_cleaned.drop(columns=['price'])
    context_data = features.iloc[0].to_dict()
    predicted_price = get_predict_price(data)
    return real_price, context_data, predicted_price

# Обработка данных с CIAN
def process_cian_data(data):
    result = pd.json_normalize(data).replace({None: pd.NA})
    if isinstance(result, str):
        st.error(result)
        return None
    result = result.loc[:, ~result.columns.duplicated()]
    if 'publication_at' in result.columns:
        result['publication_at'] = pd.to_datetime(result['publication_at'], unit='s')
    result = reorder_columns(map_dataframe(result, direction="to_russian"))
    return result