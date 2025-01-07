from logger_setup import setup_logger
import pandas as pd
import streamlit as st
import json
import httpx
from io import BytesIO

logger = setup_logger()

# Рассчитывает разницу и процентное отклонение между предсказанной и реальной стоимостью
def calculate_difference(predicted_price, real_price):
    difference = predicted_price - real_price
    difference_percent = (difference / real_price) * 100
    return difference, difference_percent

# Загружает пользовательский датасет и проверяет его соответствие структуре дефолтного датасета
def load_user_dataset(uploaded_file, cleaned_dataset):
    try:
        logger.info("Пользователь загрузил свой датасет")
        user_df = pd.read_csv(uploaded_file)
        if set(user_df.columns) != set(cleaned_dataset.columns):
            raise ValueError("Структура загруженного датасета не соответствует дефолтному датасету.")
        return user_df
    except Exception as e:
        logger.error(f"Ошибка при загрузке пользовательского датасета: {e}")
        st.error(f"Ошибка: {e}")
        return None

# Загрузка набора данных с URL
@st.cache_data
def load_dataset_from_url(dataset_url):
    try:
        logger.info(f"Загрузка набора данных с URL: {dataset_url}")
        with httpx.Client(follow_redirects=True) as client:
            response = client.get(dataset_url)
            response.raise_for_status()
        file = BytesIO(response.content)
        return pd.read_csv(file)
    except Exception as e:
        logger.error(f"Ошибка загрузки набора данных: {e}")
        st.error(f"Ошибка: {e}")
        st.stop()

# Загрузка конфигурационного файла
@st.cache_data
def load_config(config_path):
    try:
        logger.info(f"Загрузка конфигурационного файла: {config_path}")
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"Файл {config_path} не найден. Проверьте путь.")
        st.error(f"Файл {config_path} не найден. Проверьте путь.")
        st.stop()
    except json.JSONDecodeError as e:
        logger.error(f"Ошибка чтения JSON-файла: {e}")
        st.error(f"Ошибка чтения JSON-файла: {e}")
        st.stop()

# Обрабатывает загрузку файла и возвращает пользовательский датасет или дефолтный, если файл не загружен или имеет ошибку
def handle_file_upload(uploaded_file, cleaned_dataset):
    if uploaded_file:
        user_dataset = load_user_dataset(uploaded_file, cleaned_dataset)
        if user_dataset is not None:
            st.success("Датасет успешно загружен!")
            return user_dataset
        else:
            st.error("Ошибка в загруженном датасете. Используется датасет по умолчанию.")
    else:
        st.info("Используется датасет по умолчанию.")
    return cleaned_dataset