import json
import streamlit as st
from streamlit_api_client import get_data_page, get_predict_price, calculate_difference, map_feature_values

# Интерфейс Streamlit
st.title("Прогноз стоимости квартиры")
st.sidebar.header("Выберите режим")
mode = st.sidebar.radio("Режим работы", ["Прогноз стоимости по ссылке cian", "Прогноз стоимости по параметрам"])

# Читаем данные JSON
with open('data_config.json', 'r', encoding='utf-8') as f:
    loaded_data = json.load(f)

limits = loaded_data['limits']
categories = loaded_data['categories']

if mode == "Прогноз стоимости по ссылке cian":
    st.subheader("Прогноз стоимости по ссылке")
    cian_url = st.text_input("Введите ссылку на объявление cian")

    if cian_url:
        result = get_data_page(cian_url)
        if isinstance(result, str):
            st.subheader("Ошибка")
            st.write(result)
        else:
            st.subheader("Полученные данные")
            st.dataframe(result)
            
            features = result.drop(columns=['price'])
            real_price = float(result['price'].iloc[0])
            
            input_json = features.to_dict(orient="records")[0]
            predicted_price = get_predict_price(input_json)
            
            if isinstance(predicted_price, str):
                st.subheader("Ошибка")
                st.write(predicted_price)
            else:
                difference, difference_percent = calculate_difference(predicted_price, real_price)

                st.subheader("Результаты прогнозирования")
                st.write(f"Предсказанная стоимость: {predicted_price:.2f} ₽")
                st.write(f"Реальная стоимость: {real_price:.2f} ₽")
                st.write(f"Разница прогнозной стоимости от реальной: {difference:.2f} ₽ ({difference_percent:.2f}%)")

                if difference > 0:
                    st.success(f"Выгодно покупать. Экономия {difference:.2f} ₽.")
                else:
                    st.error(f"Не выгодно покупать. Переплата {-difference:.2f} ₽.")

elif mode == "Прогноз стоимости по параметрам":  
    st.subheader("Прогноз стоимости по параметрам")

    st.subheader("Основные параметры квартиры")
    total_area = st.slider("Общая площадь (м²)", min_value=limits['total_area']['min'], max_value=limits['total_area']['max'], value=limits['total_area']['default_value'], step=1)
    rooms_count = st.slider("Количество комнат", min_value=limits['rooms_count']['min'], max_value=limits['rooms_count']['max'], value=limits['rooms_count']['default_value'], step=1)

    st.subheader("Местоположение")
    district = st.selectbox("Район", categories['district']['data'], index=categories['district']['data'].index(categories['district']['default_value']))
    metro = st.selectbox("Ближайшее метро", categories['metro']['data'], index=categories['metro']['data'].index(categories['metro']['default_value']))
    distance_from_center = st.slider("Расстояние до центра (км)", min_value=limits['distance_from_center']['min'], max_value=limits['distance_from_center']['max'], value=limits['distance_from_center']['default_value'], step=0.1)

    st.subheader("Параметры дома")
    build_year = st.slider("Год постройки", min_value=limits['build_year']['min'], max_value=limits['build_year']['max'], value=limits['build_year']['default_value'], step=1)
    floor_number = st.slider("Этаж", min_value=limits['floor_number']['min'], max_value=limits['floor_number']['max'], value=limits['floor_number']['default_value'], step=1)
    material_type = st.selectbox("Тип материала", categories['material_type']['data'], index=categories['material_type']['data'].index(categories['material_type']['default_value']))
    county = st.selectbox("Округ", categories['county']['data'], index=categories['county']['data'].index(categories['county']['default_value']))

    st.subheader("Параметры квартиры")
    flat_type = st.selectbox("Тип квартиры", categories['flat_type']['data'], index=categories['flat_type']['data'].index(categories['flat_type']['default_value']))
    repair_type = st.selectbox("Тип ремонта", categories['repair_type']['data'], index=categories['repair_type']['data'].index(categories['repair_type']['default_value']))

    st.subheader("Транспортная доступность")
    travel_type = st.radio("Способ передвижения", options=categories['travel_type']['data'], index=categories['travel_type']['data'].index(categories['travel_type']['default_value']))
    travel_time = st.slider("Время в пути (мин)", min_value=limits['travel_time']['min'], max_value=limits['travel_time']['max'], value=limits['travel_time']['default_value'], step=1)


    # Прогноз
    if st.button("Прогнозировать стоимость"):
        mapped_values = map_feature_values(material_type, flat_type, repair_type)

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

        predicted_price = get_predict_price(input_data)

        if isinstance(predicted_price, str):
            st.subheader("Ошибка")
            st.write(predicted_price)
        else:
            st.subheader("Результаты прогнозирования")
            st.write(f"Предсказанная стоимость: {predicted_price:.2f} ₽")
