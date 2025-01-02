import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
import pandas as pd

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
        yaxis=dict(showgrid=True),
        legend=dict(title="Легенда")
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

    fig_rooms_price.update_layout(legend=dict(title="Легенда"))
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
        yaxis=dict(showgrid=True, gridcolor='rgba(200, 200, 200, 0.3)'),
        legend=dict(title="Легенда")
    )

    graphs.append(fig_district_price)

    # 5. Карта
    if is_real and 'coordinates.lat' in context_data and 'coordinates.lng' in context_data:
        lat = context_data['coordinates.lat']
        lng = context_data['coordinates.lng']
        
        if lat is not None and lng is not None:
            fig_map = px.scatter_mapbox(
                lat=[lat],
                lon=[lng],
                hover_name=["Объект"],
                color=["Объект"],
                size=[5],
                size_max=10,
                zoom=12,
                mapbox_style="open-street-map",
                color_discrete_sequence=["red"]
            )
            fig_map.update_layout(title="Местоположение квартиры", legend=dict(title="Легенда"))
            graphs.append(fig_map)

    # 6. Сравнение с медианой и средним
    median_data = {
        "Общая площадь (м²)": df['total_area'].median(),
        "Количество комнат": df['rooms_count'].median(),
        "Расстояние до центра (Мест)": round(df['distance_from_center'].median(), 1),
        "Год постройки": df['build_year'].median()
    }

    mean_data = {
        "Общая площадь (м²)": round(df['total_area'].mean(), 1),
        "Количество комнат": round(df['rooms_count'].mean()),
        "Расстояние до центра (км)": round(df['distance_from_center'].mean(), 1),
        "Год постройки": round(df['build_year'].mean())
    }

    user_data = {
        "Общая площадь (м²)": float(context_data.get('total_area', 'N/A')) if pd.notna(context_data.get('total_area', None)) else 'N/A',
        "Количество комнат": int(context_data.get('rooms_count', 'N/A')) if pd.notna(context_data.get('rooms_count', None)) else 'N/A',
        "Расстояние до центра (км)": float(context_data.get('distance_from_center', 'N/A')) if pd.notna(context_data.get('distance_from_center', None)) else 'N/A',
        "Год постройки": int(context_data.get('build_year', 'N/A')) if pd.notna(context_data.get('build_year', None)) else 'N/A'
    }

    comparison_df = pd.DataFrame([user_data, median_data, mean_data], index=["Данные из объявления", "Медиана по рынку", "Среднее по рынку"])

    st.write("Сравнение параметров с медианой и средним по датасету")
    st.dataframe(comparison_df)

    return graphs


def calculate_difference(predicted_price, real_price):
    """Рассчитывает разницу и процентное отклонение"""
    difference = predicted_price - real_price
    difference_percent = (difference / real_price) * 100
    return difference, difference_percent
