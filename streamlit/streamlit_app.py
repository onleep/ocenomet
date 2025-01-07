import json
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
import io
from datetime import datetime
from logger_setup import setup_logger
from mapping_utils import map_values
from visualization import analyze_and_display_results
from tools import handle_file_upload, load_dataset_from_url, load_config
from api_client import *

logger = setup_logger()

# Инициализация состояния приложения
def initialize_state():
    if "last_mode" not in st.session_state:
        st.session_state["last_mode"] = None
    if "show_model_settings" not in st.session_state:
        st.session_state["show_model_settings"] = False
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "main"

# Управление переключением страниц
def main_page():
    st.session_state["current_page"] = "main"

def settings_page():
    st.session_state["current_page"] = "settings"

# Рендерит интерфейс для предсказания стоимости по ссылке на Cian
def render_cian_prediction_page(working_dataset):
    st.subheader("Прогноз стоимости по ссылке")
    cian_url = st.text_input("Введите ссылку на объявление cian")

    if cian_url:
        data = fetch_data(cian_url)
        if data is not None:
            result = process_cian_data(data)
            st.subheader("Полученные данные")
            st.dataframe(result)
            
            real_price, context_data, predicted_price = get_real_and_predicted_prices(result, data)
            if isinstance(predicted_price, str):
                    st.subheader("Ошибка")
                    st.error(predicted_price)
            else:
                analyze_and_display_results(predicted_price=predicted_price, working_dataset=working_dataset, context_data=context_data, real_price=real_price)

# Получает ручной ввод пользователя для настройки параметров квартиры.
def get_user_input(data_config):
    with st.expander("Параметры квартиры", expanded=True):
        with st.form("input_form"):
            st.subheader("Основные параметры квартиры")

            limits = data_config['limits']
            categories = data_config['categories']

            try:
                # Ввод параметров недвижимости
                total_area = st.slider(
                    "Общая площадь (м²)",
                    min_value=limits['total_area']['min'],
                    max_value=limits['total_area']['max'],
                    value=limits['total_area']['default_value'],
                    step=1
                )
                rooms_count = st.slider(
                    "Количество комнат",
                    min_value=limits['rooms_count']['min'],
                    max_value=limits['rooms_count']['max'],
                    value=limits['rooms_count']['default_value'],
                    step=1
                )
                flat_type = st.selectbox(
                    "Тип квартиры",
                    categories['flat_type']['data'],
                    index=categories['flat_type']['data'].index(categories['flat_type']['default_value'])
                )
                repair_type = st.selectbox(
                    "Тип ремонта",
                    categories['repair_type']['data'],
                    index=categories['repair_type']['data'].index(categories['repair_type']['default_value'])
                )

                st.subheader("Местоположение")
                district = st.selectbox(
                    "Район",
                    categories['district']['data'],
                    index=categories['district']['data'].index(categories['district']['default_value'])
                )
                metro = st.selectbox(
                    "Ближайшее метро",
                    categories['metro']['data'],
                    index=categories['metro']['data'].index(categories['metro']['default_value'])
                )
                distance_from_center = st.slider(
                    "Расстояние до центра (км)",
                    min_value=float(limits['distance_from_center']['min']),
                    max_value=float(limits['distance_from_center']['max']),
                    value=float(limits['distance_from_center']['default_value']),
                    step=0.1
                )

                st.subheader("Параметры дома")
                build_year = st.slider(
                    "Год постройки",
                    min_value=limits['build_year']['min'],
                    max_value=limits['build_year']['max'],
                    value=limits['build_year']['default_value'],
                    step=1
                )
                floor_number = st.slider(
                    "Этаж",
                    min_value=limits['floor_number']['min'],
                    max_value=limits['floor_number']['max'],
                    value=limits['floor_number']['default_value'],
                    step=1
                )
                material_type = st.selectbox(
                    "Тип материала",
                    categories['material_type']['data'],
                    index=categories['material_type']['data'].index(categories['material_type']['default_value'])
                )
                county = st.selectbox(
                    "Округ",
                    categories['county']['data'],
                    index=categories['county']['data'].index(categories['county']['default_value'])
                )

                floors_count = st.slider(
                    "Кол-во этажей",
                    min_value=limits['floors_count']['min'],
                    max_value=limits['floors_count']['max'],
                    value=limits['floors_count']['default_value'],
                    step=1
                )

                st.subheader("Транспортная доступность")
                travel_type = st.radio(
                    "Способ передвижения",
                    options=categories['travel_type']['data'],
                    index=categories['travel_type']['data'].index(categories['travel_type']['default_value'])
                )
                travel_time = st.slider(
                    "Время до метро (мин)",
                    min_value=limits['travel_time']['min'],
                    max_value=limits['travel_time']['max'],
                    value=limits['travel_time']['default_value'],
                    step=1
                )
                logger.debug("Параметры квартиры успешно введены пользователем")
            except Exception as e:
                logger.error(f"Ошибка при вводе параметров: {e}")
                st.error(f"Ошибка: {e}")

            submit_button = st.form_submit_button("Прогнозировать стоимость")

        if submit_button:
            logger.info("Пользователь нажал кнопку 'Прогнозировать стоимость'")
            mapped_values = map_values(material_type, flat_type, repair_type, travel_type)
            current_date = datetime.now()
            timestamp = int(current_date.timestamp())

            input_data = {
                "total_area": total_area,
                "rooms_count": rooms_count,
                "metro": metro,
                "distance_from_center": distance_from_center,
                "district": district,
                "build_year": build_year,
                "floor_number": floor_number,
                "floors_count": floors_count,
                "material_type": mapped_values["material_type"],
                "county": county,
                "flat_type": mapped_values["flat_type"],
                "repair_type": mapped_values["repair_type"],
                "travel_type": mapped_values["travel_type"],
                "travel_time": travel_time,
                "publication_at": timestamp
            }
            logger.debug(f"Данные для предсказания: {input_data}")
            return input_data

# Рендерит интерфейс для ввода пользовательских параметров квартиры
def render_custom_parameters_page(working_dataset, data_config):
    st.subheader("Прогноз стоимости по своим параметрам")
    input_data = get_user_input(data_config)
    if input_data is not None:
        try:
            predicted_price = get_predict_price(input_data)

            if isinstance(predicted_price, str):
                logger.error(f"Ошибка при предсказании стоимости: {predicted_price}")
                st.subheader("Ошибка")
                st.write(predicted_price)
            else:
                analyze_and_display_results(
                    predicted_price=predicted_price,
                    working_dataset=working_dataset,
                    context_data=input_data,
                    real_price=None
                )
        except Exception as e:
            logger.error(f"Ошибка при обработке данных для прогноза: {e}")
            st.error(f"Ошибка: {e}")

# Главная страница приложения
def render_main_page(cleaned_dataset, data_config):
    st.title("Предскажи стоимость квартиры")
    st.sidebar.header("Выберите режим")
    mode = st.sidebar.radio("Режим работы", ["Прогноз стоимости по ссылке cian", "Прогноз стоимости по своим параметрам"])

    working_dataset = cleaned_dataset

    expander = st.sidebar.expander("Настройки", expanded=False)
    with expander:
        st.subheader("📂 Датасет")
        st.caption("Загрузка своего датасета.")
        uploaded_file = st.file_uploader("Выберите файл (CSV):", type="csv")
        working_dataset = handle_file_upload(uploaded_file, cleaned_dataset)

        st.subheader("🔧 Модели")
        st.caption("Управление своими моделями.")
        st.button("Открыть настройки моделей", on_click=settings_page)

    if mode == "Прогноз стоимости по ссылке cian":
        render_cian_prediction_page(working_dataset)
    elif mode == "Прогноз стоимости по своим параметрам":
        render_custom_parameters_page(working_dataset, data_config)

# Страница настроек модели
def render_settings_page():
    st.title("Настройки моделей")
    st.sidebar.button("Вернуться назад", on_click=main_page)

    st.subheader("Создание новой модели и выбор гиперпараметров")
    model_id = st.text_input("Введите ID модели", "")
    model_type = st.selectbox("Выберите тип модели", ["ls", "lr", "rg"], help="lr - LinearRegression, ls - Lasso, rg - Ridge")
    hyperparameters = st.text_area(
        "Введите гиперпараметры в формате JSON",
        '{"alpha": 0.1}',
        help="Ожидается JSON-объект (пример: {\"param1\": 0.1, \"param2\": 5})"
    )
    
    X_data = st.text_area(
        "Введите данные X (в формате JSON)",
        '[{"example_1": 2, "example_2": 3}]',
        help="Ожидается JSON массив объектов (пример: [{\"example_1\": 2, \"example_2\": 3}])"
    )
    
    y_data = st.text_area(
        "Введите данные y (в формате JSON)",
        "[1, 3, 4]",
        help="Ожидается JSON массив (пример: [1, 2, 3])"
    )
    
    if st.button("Создать и обучить модель"):
        if not model_id or not X_data or not y_data:
            st.error("Пожалуйста, заполните все поля.")
        else:
            try:
                X = pd.read_json(io.StringIO(X_data))
                y = pd.read_json(io.StringIO(y_data))
                try:
                    hyperparams = json.loads(hyperparameters)
                except json.JSONDecodeError as e:
                    hyperparams = {}
                
                result = fit_model(model_id, model_type, hyperparams, X.to_numpy(), y.to_numpy().ravel())
                if isinstance(result, list) and len(result) > 0 and isinstance(result[0], dict) and "message" in result[0]:
                    st.success("Модель успешно обучена!")
                    st.write(result[0]["message"])
                elif isinstance(result, dict):
                    st.success("Модель успешно обучена!")
                    st.json(result)
                else:
                    st.error(f"Ошибка: {result}")
            except Exception as e:
                st.error(f"Ошибка: {e}")

    st.divider()

    # Показ данных моделей
    st.subheader("Характеристики моделей")
    if st.button("Показать данные моделей"):
        models_info = list_models()

        if isinstance(models_info, str):
            st.error(models_info)
        else:
            for model_data in models_info:
                models = model_data.get("models", [])
                if not models:
                    st.write("Нет доступных моделей.")
                    continue

                for model_data in models_info:
                    models = model_data.get("models", [])
                    if not models:
                        st.write("Нет доступных моделей.")
                        continue

                    for model in models:
                        params = model.get('params', {})
                        st.subheader(f"Модель ID: {model.get('id', 'N/A')}")
                        st.write(f"Тип модели: {params.get('model_type', 'N/A')}")

                        st.write("Гиперпараметры:")
                        hyperparameters = params.get('hyperparameters', {})
                        st.json(hyperparameters)

                        st.write("Метрики:")
                        st.write(f"  - R2 Score: {params.get('r2', 'N/A')}")
                        st.write(f"Время обучения: {params.get('train_time', 'N/A')} секунд")

                        # Кривая обучения
                        learning_curve = params.get('learning_curve', {})
                        if learning_curve:
                            train_sizes = learning_curve.get('train_sizes', [])
                            r2_train_scores = learning_curve.get('r2_train_scores', [])
                            r2_train_scores = learning_curve.get('r2_test_scores', [])

                            if train_sizes and r2_train_scores and r2_train_scores:
                                fig = go.Figure()
                                fig.add_trace(go.Scatter(
                                    x=train_sizes,
                                    y=r2_train_scores,
                                    mode='lines+markers',
                                    name='Train Score'
                                ))
                                fig.add_trace(go.Scatter(
                                    x=train_sizes,
                                    y=r2_train_scores,
                                    mode='lines+markers',
                                    name='Test Score'
                                ))
                                fig.update_layout(
                                    title=f"Кривая обучения для модели {model.get('id', 'N/A')} (R²: {params.get('r2', 'N/A')})",
                                    xaxis_title='Размер обучающей выборки',
                                    yaxis_title='Средний R²',
                                    legend_title='Тип данных',
                                    template='plotly_white'
                                )
                                st.plotly_chart(fig)
                            else:
                                st.write("Недостаточно данных для отображения кривой обучения.")
                        else:
                            st.write("Кривая обучения отсутствует.")


    st.divider()

    # Загрузка модели
    st.subheader("Загрузка модели")
    load_model_id = st.text_input("Введите ID модели для загрузки", key="load_model_id")
    if st.button("Загрузить модель"):
        if not load_model_id:
            st.error("Введите ID модели.")
        else:
            result = load_model(load_model_id)
            if isinstance(result, list) and len(result) > 0 and isinstance(result[0], dict) and "message" in result[0]:
                st.success(result[0]["message"])
            elif isinstance(result, str):
                st.error(result)
            else:
                st.error(f"Неизвестный формат результата: {result}")

    st.divider()
    
    # Выгрузка модели
    st.subheader("Выгрузить модель")
    if st.button("Выгрузить модель"):
        result = unload_model()
        if isinstance(result, list) and len(result) > 0 and isinstance(result[0], dict) and "message" in result[0]:
            st.success(result[0]["message"])
        elif isinstance(result, str):
            st.error(result)
        else:
            st.error(f"Неизвестный формат результата: {result}")

    st.divider()

    # Удаление модели
    st.subheader("Удаление модели")
    delete_model_id = st.text_input("Введите ID модели для удаления", key="delete_model_id")
    if st.button("Удалить модель"):
        if not delete_model_id:
            st.error("Введите ID модели.")
        else:
            result = remove_model(delete_model_id)
            if isinstance(result, list) and len(result) > 0 and isinstance(result[0], dict) and "message" in result[0]:
                st.success(result[0]["message"])
            elif isinstance(result, str):
                st.error(result)
            else:
                st.error(f"Неизвестный формат результата: {result}")

    st.divider()

    # Удаление всех моделей
    st.subheader("Удаление всех моделей")
    if st.button("Удалить все модели"):
        result = remove_all_models()
        if isinstance(result, list) and len(result) > 0 and isinstance(result[0], dict) and "message" in result[0]:
            messages = [res["message"] for res in result if "message" in res]
            for message in messages:
                st.success(message)
        elif isinstance(result, str):
            st.error(result)
        else:
            st.error(f"Неизвестный формат результата: {result}")

    st.divider()

def main():
    initialize_state()

    DATASET_URL = st.secrets["DATASET_URL"]
    cleaned_dataset = load_dataset_from_url(DATASET_URL)
    data_config = load_config(os.path.join(os.getcwd(), 'streamlit', 'data_config.json'))

    if st.session_state["current_page"] == "main":
        render_main_page(cleaned_dataset, data_config)
    elif st.session_state["current_page"] == "settings":
        render_settings_page()

if __name__ == "__main__":
    main()