import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from logger_setup import setup_logger
from tools import calculate_difference

logger = setup_logger()


# Создает визуализации для анализа данных, таких как распределение цен,
# взаимосвязь параметров с ценой и сравнительный анализ.
def create_common_graphs(df, context_data, price=None, is_real=True):
    graphs = []
    price_label = "Реальная стоимость" if is_real else "Прогнозная стоимость"

    # График распределения цен
    fig_price = px.histogram(
        df,
        x="price",
        title="Распределение стоимости квартир",
        nbins=50,
        labels={"price": "Стоимость (₽)", "count": "Количество"},
    )

    if price is not None:
        fig_price.add_vline(
            x=price,
            line_dash="dash",
            line_color="red",
            annotation_text=price_label,
        )

    fig_price.update_layout(
        xaxis_title="Стоимость (₽)",
        yaxis_title="Количество",
        xaxis=dict(showgrid=True),
        yaxis=dict(showgrid=True),
        legend=dict(title="Легенда"),
    )
    graphs.append(fig_price)

    # Взаимосвязь площади и цены
    fig_area_price = go.Figure()
    df_aggregated = df.groupby("total_area", as_index=False).agg({"price": "mean"})

    fig_area_price.add_trace(
        go.Scatter(
            x=df_aggregated["total_area"],
            y=df_aggregated["price"],
            mode="markers",
            marker=dict(size=6, color="blue"),
            name="Данные",
        )
    )

    if "total_area" in context_data and pd.notna(context_data.get("total_area")):
        fig_area_price.add_trace(
            go.Scatter(
                x=[context_data["total_area"]],
                y=[price],
                mode="markers",
                marker=dict(size=10, color="red"),
                name=price_label,
            )
        )

    fig_area_price.update_layout(
        title="Взаимосвязь общей площади и стоимости",
        xaxis=dict(
            title="Общая площадь (м²)",
            range=[df["total_area"].min(), df["total_area"].max()],
            showgrid=True,
        ),
        yaxis=dict(
            title="Стоимость (₽)",
            range=[df["price"].min(), df["price"].max()],
            showgrid=True,
        ),
        legend=dict(title="Легенда"),
    )
    graphs.append(fig_area_price)

    # Распределение стоимости по количеству комнат
    fig_rooms_price = px.box(
        df,
        x="rooms_count",
        y="price",
        title="Распределение цен по количеству комнат",
        labels={"rooms_count": "Количество комнат", "price": "Стоимость (₽)"},
    )

    if "rooms_count" in context_data:
        fig_rooms_price.add_scatter(
            x=[context_data["rooms_count"]],
            y=[price],
            mode="markers",
            marker=dict(color="red", size=10),
            name=price_label,
        )

    fig_rooms_price.update_layout(legend=dict(title="Легенда"))
    graphs.append(fig_rooms_price)

    # Средняя стоимость по округам
    df_avg_price_by_county = df.groupby("county", as_index=False).agg({"price": "mean"})
    target_county = context_data.get("county")
    colors = [
        "red" if county == target_county else "blue"
        for county in df_avg_price_by_county["county"]
    ]

    fig_district_price = px.bar(
        df_avg_price_by_county,
        x="county",
        y="price",
        title="Средняя стоимость по округам",
        labels={"county": "Округ", "price": "Средняя стоимость (₽)"},
        text="price",
    )

    fig_district_price.update_traces(
        marker_color=colors,
        texttemplate="%{text:.2s}₽",
        textposition="outside",
    )

    fig_district_price.update_layout(
        xaxis=dict(showgrid=True, gridcolor="rgba(200, 200, 200, 0.3)"),
        yaxis=dict(showgrid=True, gridcolor="rgba(200, 200, 200, 0.3)"),
        legend=dict(title="Легенда"),
    )
    graphs.append(fig_district_price)

    # Местоположение на карте
    if is_real and "coordinates.lat" in context_data and "coordinates.lng" in context_data:
        lat = context_data["coordinates.lat"]
        lng = context_data["coordinates.lng"]

        if lat is not None and lng is not None:
            fig_map = px.scatter_mapbox(
                lat=[lat],
                lon=[lng],
                hover_name=["Объект"],
                color=["Объект"],
                size=[5],
                zoom=12,
                mapbox_style="open-street-map",
                color_discrete_sequence=["red"],
            )
            fig_map.update_layout(
                title="Местоположение квартиры",
                legend=dict(title="Легенда"),
            )
            graphs.append(fig_map)

    return graphs


# Анализирует и отображает результаты предсказания стоимости.
def analyze_and_display_results(predicted_price, working_dataset, context_data, real_price=None):
    is_real = real_price is not None

    st.subheader("Анализ данных из датасета" if is_real else "Анализ введённых данных")
    logger.info("Создание графиков для анализа")
    graphs = create_common_graphs(
        working_dataset,
        context_data=context_data,
        price=real_price if is_real else predicted_price,
        is_real=is_real,
    )
    
    for graph in graphs:
        st.plotly_chart(graph)

    if is_real:
        difference, difference_percent = calculate_difference(predicted_price, real_price)
    else:
        difference, difference_percent = None, None

    st.markdown("### 🏡 Результаты прогнозирования")
    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            label="Предсказанная стоимость",
            value=f"{predicted_price:,.2f} ₽",
            delta=f"{difference_percent:.2f}%" if is_real else None,
        )

    with col2:
        st.metric(
            label="Реальная стоимость" if is_real else "N/A",
            value=f"{real_price:,.2f} ₽" if is_real else "N/A",
        )

    st.divider()

    if is_real:
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
    else:
        st.success(f"💰 Прогнозируемая стоимость: **{predicted_price:,.2f} ₽**")
