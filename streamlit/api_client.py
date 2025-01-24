import httpx
<<<<<<< HEAD
import pandas as pd
import streamlit as st

from logger_setup import setup_logger
from mapping_utils import map_dataframe, reorder_columns

# Инициализация
API_BASE_URL = st.secrets["API_BASE_URL"]
logger = setup_logger()

# Обрабатывает ошибки HTTP-запросов.
def handle_http_error(response):
    error_message = (
        f"Код ошибки - {response.status_code}. "
        f"Тело ошибки: {response.text}"
    )
    logger.error(f"Ошибка HTTP-запроса: {error_message}")
    st.error(f"Ошибка: {error_message}")
    return None

# Получение данных с объявления Циан
def get_data_page(url):
    endpoint = f"{API_BASE_URL}/api/getparams"
=======
import numpy as np
import json
import streamlit as st

# Получение данных с объявления Циан
def get_data_page(url):
    """Получает данные с объявления Циан"""
    endpoint = "http://62.113.119.220:8000/api/getparams"
>>>>>>> main
    try:
        response = httpx.get(endpoint, params={'url': url}, timeout=120)
        response.raise_for_status()
        return response
<<<<<<< HEAD
    except httpx.HTTPStatusError as e:
        return handle_http_error(e.response)
    except Exception as e:
        logger.error(f"Неизвестная ошибка: {e}")
        st.error("Произошла неизвестная ошибка.")
        return None

# Получение предсказанной стоимости от модели
def get_predict_price(input_data):
    endpoint = f"{API_BASE_URL}/api/predict"
    try:
        response = httpx.post(endpoint, json={'data': input_data})
        response.raise_for_status()
        return float(response.json()["price"])
    except httpx.HTTPStatusError as e:
        return handle_http_error(e.response)
    except Exception as e:
        logger.error(f"Неизвестная ошибка: {e}")
        st.error("Произошла неизвестная ошибка.")
        return None

# Подготовка данных для отправки на сервер
def prepare_data(X, y):
    if isinstance(X, pd.DataFrame):
        X = X.astype(object)
        X_prepared = X.to_dict(orient="records")
    else:
        raise ValueError("X должен быть DataFrame с именованными колонками.")
    
    y_prepared = list(map(int, y))
    return X_prepared, y_prepared


# Обучение модели
def fit_model(model_id, model_type, hyperparameters, X, y):
    endpoint = f"{API_BASE_URL}/api/fit"
=======
    except Exception as e:
        return f"Произошла ошибка при запросе: {e}", None

# Получение предсказанной стоимости от модели
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
    endpoint = "http://62.113.119.220:8000/api/fit"

>>>>>>> main
    config = {
        "id": model_id,
        "ml_model_type": model_type,
        "hyperparameters": hyperparameters
    }
<<<<<<< HEAD
    X_prepared, y_prepared = prepare_data(X, y)
    payload = [{"X": X_prepared, "y": y_prepared, "config": config}]

    try:
        response = httpx.post(endpoint, json=payload, timeout=300)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        logger.error(f"Ошибка HTTP-запроса: Код ошибки - {e.response.status_code}. Тело ошибки: {e.response.text}")
        st.error(f"Ошибка HTTP-запроса: Код ошибки - {e.response.status_code}. Тело ошибки: {e.response.text}")
        return None
    except Exception as e:
        logger.error(f"Неизвестная ошибка: {e}")
        st.error(f"Произошла неизвестная ошибка: {e}")
        return None

# Получение списка всех моделей
def list_models():
    endpoint = f"{API_BASE_URL}/api/list_models"
    try:
        response = httpx.get(endpoint, timeout=60)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        return handle_http_error(e.response)
    except Exception as e:
        logger.error(f"Неизвестная ошибка: {e}")
        st.error("Произошла неизвестная ошибка.")
        return None

# Загрузка модели
def load_model(model_id):
    endpoint = f"{API_BASE_URL}/api/load"
    try:
        response = httpx.post(f"{endpoint}?id={model_id}", timeout=60)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        return handle_http_error(e.response)
    except Exception as e:
        logger.error(f"Неизвестная ошибка: {e}")
        st.error("Произошла неизвестная ошибка.")
        return None

# Выгрузка всех моделей
def unload_model():
    endpoint = f"{API_BASE_URL}/api/unload"
=======
    
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
    endpoint = "http://62.113.119.220:8000/api/list_models"
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
    endpoint = "http://62.113.119.220:8000/api/load"
    try:
        response = httpx.post(endpoint, json={"id": model_id}, timeout=60)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return f"Ошибка при загрузке модели: {e}"

# Выгрузка всех моделей
def unload_model():
    """Выгружает все модели"""
    endpoint = "http://62.113.119.220:8000/api/unload"
>>>>>>> main
    try:
        response = httpx.post(endpoint, timeout=60)
        response.raise_for_status()
        return response.json()
<<<<<<< HEAD
    except httpx.HTTPStatusError as e:
        return handle_http_error(e.response)
    except Exception as e:
        logger.error(f"Неизвестная ошибка: {e}")
        st.error("Произошла неизвестная ошибка.")
        return None

# Удаление конкретной модели
def remove_model(model_id):
    endpoint = f"{API_BASE_URL}/api/remove/{model_id}"
=======
    except Exception as e:
        return f"Ошибка при выгрузке моделей: {e}"

# Удаление конкретной модели
def remove_model(model_id):
    """Удаляет модель"""
    endpoint = f"http://62.113.119.220:8000/api/remove/{model_id}"
>>>>>>> main
    try:
        response = httpx.delete(endpoint, timeout=60)
        response.raise_for_status()
        return response.json()
<<<<<<< HEAD
    except httpx.HTTPStatusError as e:
        return handle_http_error(e.response)
    except Exception as e:
        logger.error(f"Неизвестная ошибка: {e}")
        st.error("Произошла неизвестная ошибка.")
        return None

# Удаление всех моделей
def remove_all_models():
    endpoint = f"{API_BASE_URL}/api/remove_all"
=======
    except Exception as e:
        return f"Ошибка при удалении модели: {e}"

# Удаление всех моделей
def remove_all_models():
    """Удаляет все модели"""
    endpoint = "http://62.113.119.220:8000/api/remove_all"
>>>>>>> main
    try:
        response = httpx.delete(endpoint, timeout=60)
        response.raise_for_status()
        return response.json()
<<<<<<< HEAD
    except httpx.HTTPStatusError as e:
        return handle_http_error(e.response)
    except Exception as e:
        logger.error(f"Неизвестная ошибка: {e}")
        st.error("Произошла неизвестная ошибка.")
        return None

# Получение данных с CIAN
@st.cache_data
def fetch_data(cian_url):
    try:
        logger.info(f"Получение данных с CIAN по ссылке: {cian_url}")
        response = get_data_page(cian_url)
        return response.json() if response else None
    except Exception as e:
        logger.error(f"Ошибка при получении данных с CIAN: {e}")
        st.error("Произошла ошибка при получении данных.")
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
    try:
        result = pd.json_normalize(data).replace({None: pd.NA})
        result = result.loc[:, ~result.columns.duplicated()]
        if 'publication_at' in result.columns:
            result['publication_at'] = pd.to_datetime(
                result['publication_at'], unit='s'
            )
        return reorder_columns(map_dataframe(result, direction="to_russian"))
    except Exception as e:
        logger.error(f"Ошибка обработки данных CIAN: {e}")
        st.error("Ошибка обработки данных.")
        return None
=======
    except Exception as e:
        return f"Ошибка при удалении всех моделей: {e}"
>>>>>>> main
