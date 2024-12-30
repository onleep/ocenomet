import json
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import os
import requests
from io import BytesIO
from api_client import get_data_page, get_predict_price
from mapping_utils import map_values, map_dataframe, reorder_columns

def create_common_graphs(df, context_data, price=None, is_real=True):
    graphs = []
    price_label = "Реальная стоимость" if is_real else "Прогнозная стоимость"

    # 1. График распределения цен
    fig_price = px.histogram(
        df,
        x='price',
        title='Распределение стоимости квартир',
        nbins=50,
        labels={'price': 'Стоимость (₽)', 'count': 'Количество'}
    )

    if price is not None:
        fig_price.add_vline(
            x=price,
            line_dash="dash",
            line_color="red",
            annotation_text=price_label
        )

    fig_price.update_layout(
        xaxis_title='Стоимость (₽)',
        yaxis_title='Количество',
        xaxis=dict(showgrid=True),
        yaxis=dict(showgrid=True)
    )

    graphs.append(fig_price)

    # 2. Взаимосвязь площади и цены
    fig_area_price = go.Figure()
    df_aggregated = df.groupby('total_area', as_index=False).agg({'price': 'mean'})

    fig_area_price.add_trace(
        go.Scatter(
            x=df_aggregated['total_area'],
            y=df_aggregated['price'],
            mode='markers',
            marker=dict(size=6, color='blue'),
            name='Данные'
        )
    )

    if 'total_area' in context_data and pd.notna(context_data.get('total_area')) and price is not None:
        current_total_area = float(context_data.get('total_area', 0))
        current_price = float(price)

        fig_area_price.add_trace(
            go.Scatter(
                x=[current_total_area],
                y=[current_price],
                mode='markers',
                marker=dict(size=10, color='red'),
                name=price_label
            )
        )

    fig_area_price.update_layout(
        title='Взаимосвязь общей площади и стоимости',
        xaxis=dict(title='Общая площадь (м²)', range=[df['total_area'].min(), df['total_area'].max()], showgrid=True),
        yaxis=dict(title='Стоимость (₽)', range=[df['price'].min(), df['price'].max()], showgrid=True),
        legend=dict(title="Легенда")
    )

    graphs.append(fig_area_price)

    # 3. Количество комнат и стоимость
    fig_rooms_price = px.box(
        df,
        x='rooms_count',
        y='price',
        title='Распределение цен по количеству комнат',
        labels={'rooms_count': 'Количество комнат', 'price': 'Стоимость (₽)'}
    )
    if 'rooms_count' in context_data and price is not None:
        fig_rooms_price.add_scatter(
            x=[context_data.get('rooms_count', 0)],
            y=[price],
            mode='markers',
            marker=dict(color='red', size=10),
            name=price_label
        )
    graphs.append(fig_rooms_price)

    # 4. Влияние целевой округ и стоимости
    df_avg_price_by_county = df.groupby('county', as_index=False).agg({'price': 'mean'})
    target_county = context_data.get('county', None)
    colors = ['red' if county == target_county else 'blue' for county in df_avg_price_by_county['county']]

    fig_district_price = px.bar(
        df_avg_price_by_county,
        x='county',
        y='price',
        title='Средняя стоимость по округам',
        labels={'county': 'Округ', 'price': 'Средняя стоимость (₽)'},
        text='price'
    )

    fig_district_price.update_traces(
        marker_color=colors,
        texttemplate='%{text:.2s}₽',
        textposition='outside'
    )

    fig_district_price.update_layout(
        xaxis=dict(showgrid=True, gridcolor='rgba(200, 200, 200, 0.3)'),
        yaxis=dict(showgrid=True, gridcolor='rgba(200, 200, 200, 0.3)')
    )

    graphs.append(fig_district_price)


    # 5. Сравнение с медианой
    median_data = {
        "Общая площадь (м²)": df['total_area'].median(),
        "Количество комнат": df['rooms_count'].median(),
        "Расстояние до центра (км)": df['distance_from_center'].median(),
        "Год постройки": df['build_year'].median()
    }
    user_data = {
        "Общая площадь (м²)": float(context_data.get('total_area', 'N/A')) if pd.notna(context_data.get('total_area', None)) else 'N/A',
        "Количество комнат": int(context_data.get('rooms_count', 'N/A')) if pd.notna(context_data.get('rooms_count', None)) else 'N/A',
        "Расстояние до центра (км)": float(context_data.get('distance_from_center', 'N/A')) if pd.notna(context_data.get('distance_from_center', None)) else 'N/A',
        "Год постройки": int(context_data.get('build_year', 'N/A')) if pd.notna(context_data.get('build_year', None)) else 'N/A'
    }
    comparison_df = pd.DataFrame([user_data, median_data], index=["Данные из объявления", "Медиана по рынку"])
    st.write("Сравнение введённых параметров с медианой по датасету")
    st.dataframe(comparison_df)

    return graphs

def calculate_difference(predicted_price, real_price):
    """Рассчитывает разницу и процентное отклонение"""
    difference = predicted_price - real_price
    difference_percent = (difference / real_price) * 100
    return difference, difference_percent

@st.cache_data
def load_dataset_from_url(dataset_url):
    try:
        response = requests.get(dataset_url)
        response.raise_for_status()

        # Чтение файла как CSV из бинарного потока
        file = BytesIO(response.content)
        return pd.read_csv(file)
    except requests.exceptions.RequestException as e:
        st.error(f"Ошибка загрузки датасета: {e}")
        st.stop()
    except pd.errors.ParserError as e:
        st.error(f"Ошибка чтения CSV-файла: {e}")
        st.stop()

@st.cache_data
def load_config(config_path):
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error(f"Файл {config_path} не найден. Проверьте путь.")
        st.stop()
    except json.JSONDecodeError as e:
        st.error(f"Ошибка чтения JSON-файла: {e}")
        st.stop()

@st.cache_data
def fetch_data(cian_url):
    return get_data_page(cian_url)

DATASET_URL = st.secrets["DATASET_URL"]  # URL к файлу в облаке

cleaned_dataset = load_dataset_from_url(DATASET_URL)
data_config = load_config(os.path.join(os.getcwd(), 'streamlit', 'data_config.json'))

limits = data_config['limits']
categories = data_config['categories']

# Интерфейс Streamlit
st.title("Предскажи стоимость квартиры")
st.sidebar.header("Выберите режим")
mode = st.sidebar.radio("Режим работы", ["Прогноз стоимости по ссылке cian", "Прогноз стоимости по своим параметрам"])

if mode == "Прогноз стоимости по ссылке cian":
    st.subheader("Прогноз стоимости по ссылке")
    cian_url = st.text_input("Введите ссылку на объявление cian")

    if cian_url:
        result = fetch_data(cian_url)
        result = reorder_columns(map_dataframe(result, direction="to_russian"))
        
        if isinstance(result, str):
            st.subheader("Ошибка")
            st.write(result)
        else:
            st.subheader("Полученные данные")
            st.dataframe(result)

            result = map_dataframe(result, direction="to_english")
            result_cleaned = result.dropna(axis=1)

            features = result_cleaned.drop(columns=['price'])
            real_price = float(result['price'].iloc[0])
            context_data = features.iloc[0].to_dict()
            input_json = features.to_dict(orient="records")[0]

            predicted_price = get_predict_price(input_json)

            st.subheader("Анализ данных из датасета")
            graphs = create_common_graphs(cleaned_dataset, context_data=context_data, price=real_price, is_real=True)
            for graph in graphs:
                st.plotly_chart(graph)

            if isinstance(predicted_price, str):
                st.subheader("Ошибка")
                st.error(predicted_price)
            else:
                difference, difference_percent = calculate_difference(predicted_price, real_price)

                st.markdown("### 🏡 Результаты прогнозирования")
                col1, col2 = st.columns(2)

                with col1:
                    st.metric(
                        label="Предсказанная стоимость",
                        value=f"{predicted_price:,.2f} ₽",
                        delta=f"{difference_percent:.2f}%" if difference_percent != 0 else None
                    )

                with col2:
                    st.metric(
                        label="Реальная стоимость",
                        value=f"{real_price:,.2f} ₽"
                    )

                st.divider()

                if difference > 0:
                    st.success(
                        f"💰 Выгодно покупать! Экономия: **{difference:,.2f} ₽** "
                        f"(*{difference_percent:.2f}% ниже реальной стоимости*)."
                    )
                else:
                    st.error(
                        f"🚫 Не выгодно покупать! Переплата: **{-difference:,.2f} ₽** "
                        f"(*{abs(difference_percent):.2f}% выше реальной стоимости*)."
                    )

elif mode == "Прогноз стоимости по своим параметрам":  
    st.subheader("Прогноз стоимости по своим параметрам")

    with st.expander("Параметры квартиры", expanded=True):
        with st.form("input_form"):
            st.subheader("Основные параметры квартиры")
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

            submit_button = st.form_submit_button("Прогнозировать стоимость")

    if submit_button:
        mapped_values = map_values(material_type, flat_type, repair_type, travel_type)

        input_data = {
            "total_area": total_area,
            "rooms_count": rooms_count,
            "metro": metro,
            "distance_from_center": distance_from_center,
            "district": district,
            "build_year": build_year,
            "floor_number": floor_number,
            "material_type": mapped_values["material_type"],
            "county": county,
            "flat_type": mapped_values["flat_type"],
            "repair_type": mapped_values["repair_type"],
            "travel_type": mapped_values["travel_type"],
            "travel_time": travel_time
        }

        # Получение предсказанной стоимости
        predicted_price = get_predict_price(input_data)

        if isinstance(predicted_price, str):
            st.subheader("Ошибка")
            st.write(predicted_price)
        else:
            # Анализ данных
            st.subheader("Анализ введённых данных")
            graphs = create_common_graphs(cleaned_dataset, context_data=input_data, price=predicted_price, is_real=False)
            for graph in graphs:
                st.plotly_chart(graph)

            # Результаты прогнозирования
            st.subheader("Результаты прогнозирования")
            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    label="Предсказанная стоимость",
                    value=f"{predicted_price:,.2f} ₽"
                )

            with col2:
                st.metric(
                    label="Реальная стоимость",
                    value="N/A"
                )

            st.divider()
            st.success(
                f"💰 Прогнозируемая стоимость: **{predicted_price:,.2f} ₽**"
            )

