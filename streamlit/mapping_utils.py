# Маппинги для преобразования значений параметров
value_mappings = {
    "material_type": {
        "Панельный": "panel",
        "Монолитный": "monolith",
        "Блочный": "block",
        "Кирпичный": "brick",
        "Монолитно-кирпичный": "monolithBrick",
        "Сталинский": "stalin",
        "Деревянный": "wood",
    },
    "flat_type": {
        "Комнатная квартира": "rooms",
        "Студия": "studio",
        "Свободная планировка": "openPlan",
    },
    "repair_type": {
        "Евроремонт": "euro",
        "Без ремонта": "no",
        "Косметический": "cosmetic",
        "Дизайнерский": "design",
    },
    "travel_type": {
        "Пешком": "walk",
        "На транспорте": "transport",
    },
    "category": {
        "Квартира в новостройке": "newBuildingFlatSale",
        "Доля в квартире": "flatShareSale",
        "Квартира": "flatSale",
    },
    "sale_type": {
        "Свободная продажа": "free",
        "214-ФЗ": "fz214",
        "Альтернатива": "alternative",
        "Договор уступки права требования": "dupt",
        "Предварительный договор купли-продажи": "pdkp",
        "Договор ЖСК": "dzhsk",
        "Договор инвестирования": "investment",
    },
    "deal_type": {
        "Продажа": "sale",
    },
    "parking_type": {
        "Наземная": "ground",
        "Подземная": "underground",
        "Многоуровневая": "multilevel",
        "Открытая": "open",
        "На крыше": "roof",
    },
    "windows_view": {
        "На улицу и двор": "yardAndStreet",
        "Во двор": "yard",
        "На улицу": "street",
    },
    "realty_type": {
        "Квартира": "flat",
    },
    "heat_type": {
        "Центральное": "central",
        "ИТП": "itp",
        "Автоманомный котел": "autonomousBoiler",
        "Котел": "boiler",
        "Электрическое": "electric",
        "Без отопления": "without",
        "Печь": "stove",
    },
    "gas_type": {
        "Центральное": "central",
        "Автономное": "autonomous",
        "Без водоснабжения": "autonomous",
        "Неизвестно": "unknown",
    },
}

# Маппинг названий колонок
column_mapping = {
    "Округ": "county",
    "Район": "district",
    "Метро": "metro",
    "Способ передвижения": "travel_type",
    "Время до метро (мин)": "travel_time",
    "Категория": "category",
    "Кол-во просмотров": "views_count",
    "Кол-во фотографий": "photos_count",
    "Этаж": "floor_number",
    "Кол-во этажей": "floors_count",
    "Тип жилья": "flat_type",
    "Тип продажи": "sale_type",
    "Кол-во отзывов застройщика": "review_count",
    "Рейтинг застройщика ": "total_rate",
    "Тип проекта": "project_type",
    "Апартаменты": "is_apartment",
    "Пентхаус": "is_penthouse",
    "Ипотека разрешена": "is_mortgage_allowed",
    "Премиум": "is_premium",
    "Аварийное состояние": "is_emergency",
    "Реновация": "renovation_programm",
    "Тип ремонта": "repair_type",
    "Общая площадь (м²)": "total_area",
    "Жилая площадь (м²)": "living_area",
    "Площадь кухни (м²)": "kitchen_area",
    "Высота потолков (м)": "ceiling_height",
    "Кол-во балконов": "balconies",
    "Кол-во лоджий": "loggias",
    "Кол-во комнат": "rooms_count",
    "Раздельный санузел": "separated_wc",
    "Совмещённый санузел": "combined_wc",
    "Год постройки": "build_year",
    "Тип материала": "material_type",
    "Мусоропровод": "garbage_chute",
    "Расстояние до центра (км)": "distance_from_center",
    "Год публикации": "year",
    "Месяц публикации": "month",
    "День недели публикации": "day_of_week",
    "День месяца публикации": "day_of_month",
    "Стоимость": "price",
    "Название застройщика": "name",
    "Кол-во зданий застройщика": "buildings_count",
    "Год основания застройщика": "foundation_year",
    "Надежность застройщика": "is_reliable",
    "Название агентства": "agent_name",
    "Описание": "description",
    "Тип недвижимости": "realty_type",
    "Тип отопления": "heat_type",
    "Тип газа": "gas_type",
    "Кол-во подъездов": "entrances",
    "Тип парковки": "parking_type",
    "Кол-во лифтов": "lifts_count",
    "Грузовые лифты": "cargo_lifts",
    "Вид из окон": "windows_view",
    "Координаты (широта)": "coordinates.lat",
    "Координаты (долгота)": "coordinates.lng",
    "Тип сделки": "deal_type",
    "id объявления": "cian_id",
    "Улица": "street",
    "Дом": "house",
    "Кол-во пассажирских лифтов": "passenger_lifts",
    "Дата публикации": "publication_at",
    "Дата завершения строительства": "finish_date",
    "Квартал завершения строительства": "finish_date.quarter",
    "Год завершения строительства": "finish_date.year",
}

# Порядок колонок
column_order = [
    "Стоимость", "Общая площадь (м²)", "Жилая площадь (м²)", "Площадь кухни (м²)", "Кол-во комнат",
    "Этаж", "Кол-во этажей", "Год постройки", "Метро", "Время до метро (мин)", "Округ", "Район",
    "Расстояние до центра (км)", "Тип жилья", "Тип материала", "Тип ремонта", "Способ передвижения",
    "Категория", "Тип сделки", "Кол-во просмотров", "Кол-во фотографий", "Кол-во отзывов застройщика",
    "Рейтинг застройщика ", "Ипотека разрешена", "Премиум", "Аварийное состояние", "Реновация",
    "Пентхаус", "Апартаменты", "Кол-во подъездов", "Тип парковки", "Кол-во лифтов",
    "Кол-во пассажирских лифтов", "Грузовые лифты", "Вид из окон", "Кол-во балконов", "Кол-во лоджий",
    "Мусоропровод", "Высота потолков (м)", "Раздельный санузел", "Совмещённый санузел",
    "Название застройщика", "Кол-во зданий застройщика", "Год основания застройщика",
    "Надежность застройщика", "Название агентства", "Описание", "Тип недвижимости",
    "Тип отопления", "Тип газа", "Координаты (широта)", "Координаты (долгота)",
    "Год публикации", "Месяц публикации", "День недели публикации", "День месяца публикации",
    "Дата публикации", "id объявления", "Улица", "Дом",
]

# Преобразует значения параметров квартиры на основе заданных маппингов
def map_values(material_type, flat_type, repair_type, travel_type):
    return {
        "material_type": value_mappings["material_type"].get(material_type, material_type),
        "flat_type": value_mappings["flat_type"].get(flat_type, flat_type),
        "repair_type": value_mappings["repair_type"].get(repair_type, repair_type),
        "travel_type": value_mappings["travel_type"].get(travel_type, travel_type),
    }

# Преобразует названия колонок и значения DataFrame между русским и английским языками
def map_dataframe(df, direction):
    if direction not in {"to_english", "to_russian"}:
        raise ValueError("Invalid direction. Use 'to_english' or 'to_russian'.")

    if direction == "to_english":
        df = df.rename(columns=column_mapping)

    for column in df.columns:
        if column in value_mappings:
            mapping = value_mappings[column]
            selected_mapping = mapping if direction == "to_english" else {v: k for k, v in mapping.items()}
            df[column] = df[column].map(selected_mapping).fillna(df[column])

    if direction == "to_russian":
        reversed_column_mapping = {value: key for key, value in column_mapping.items()}
        df = df.rename(columns=reversed_column_mapping)
    return df

# Упорядочивает колонки DataFrame в заданном порядке, добавляя остальные в конец
def reorder_columns(df):
    valid_columns = [col for col in column_order if col in df.columns]
    remaining_columns = [col for col in df.columns if col not in valid_columns]
    return df[valid_columns + remaining_columns]