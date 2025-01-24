import json
from io import BytesIO

import pandas as pd
import streamlit as st
import httpx

from logger_setup import setup_logger

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
            raise ValueError(
                "Структура загруженного датасета не соответствует эталонному датасету."
            )

        for column in cleaned_dataset.columns:
            expected_dtype = cleaned_dataset[column].dtype

            if pd.api.types.is_numeric_dtype(expected_dtype):
                user_df[column] = pd.to_numeric(user_df[column], errors='coerce')
            
            elif pd.api.types.is_categorical_dtype(expected_dtype) or expected_dtype == 'object':
                user_df[column] = user_df[column].astype(str)

        invalid_rows = user_df.isna().any(axis=1).sum()
        user_df = user_df.dropna()

        if invalid_rows > 0:
            st.warning(f"Удалено строк с некорректными данными: {invalid_rows}")

        logger.info("Датасет успешно обработан и приведен к нужным типам")
        return user_df

    except Exception as e:
        error_message = f"Ошибка при обработке пользовательского датасета: {str(e)}"
        logger.error(error_message)
        st.error(error_message)
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
    except httpx.HTTPStatusError as e:
        error_message = (
            f"Код ошибки - {e.response.status_code}. "
            f"Тело ошибки: {e.response.text}"
        )
        logger.error(error_message)
        st.error(error_message)
        st.stop()
    except Exception as e:
        error_message = f"Неизвестная ошибка при загрузке данных: {str(e)}"
        logger.error(error_message)
        st.error(error_message)
        st.stop()


# Загрузка конфигурационного файла
@st.cache_data
def load_config(config_path):
    try:
        logger.info(f"Загрузка конфигурационного файла: {config_path}")
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError as e:
        error_message = (
            f"Файл {config_path} не найден. Проверьте путь. Ошибка: {str(e)}"
        )
        logger.error(error_message)
        st.error(error_message)
        st.stop()
    except json.JSONDecodeError as e:
        error_message = f"Ошибка чтения JSON-файла: {str(e)}"
        logger.error(error_message)
        st.error(error_message)
        st.stop()


# Обрабатывает загрузку файла и возвращает пользовательский датасет или дефолтный, если файл не загружен или имеет ошибку
def handle_file_upload(uploaded_file, cleaned_dataset):
    if uploaded_file:
        user_dataset = load_user_dataset(uploaded_file, cleaned_dataset)
        if user_dataset is not None:
            st.success("Датасет успешно загружен!")
            return user_dataset
        else:
            st.error(
                "Ошибка в загруженном датасете. Используется датасет по умолчанию."
            )
    else:
        st.info("Используется датасет по умолчанию.")
    return cleaned_dataset