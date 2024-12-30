value_mappings = {
    'material_type': {
        'Панельный': 'panel',
        'Монолитный': 'monolith',
        'Блочный': 'block',
        'Кирпичный': 'brick',
        'Монолитно-кирпичный': 'monolithBrick',
        'Сталинский': 'stalin',
        'Деревянный': 'wood'
    },
    'flat_type': {
        'Комнатная квартира': 'rooms',
        'Студия': 'studio',
        'Свободная планировка': 'openPlan'
    },
    'repair_type': {
        'Евроремонт': 'euro',
        'Без ремонта': 'no',
        'Косметический': 'cosmetic',
        'Дизайнерский': 'design'
    },
    'travel_type': {
        'Пешком': 'walk',
        'На транспорте': 'transport'
    },
    'category': {
        'Квартира в новостройке': 'newBuildingFlatSale',
        'Доля в квартире': 'flatShareSale',
        'Квартира': 'flatSale'
    },
    'sale_type': {
        'Свободная продажа': 'free',
        '214-ФЗ': 'fz214',
        'Альтернатива': 'alternative',
        'Договор уступки права требования': 'dupt',
        'Предварительный договор купли-продажи': 'pdkp',
        'Договор ЖСК': 'dzhsk',
        'Договор инвестирования': 'investment'
    }
}

column_mapping = {
    'Округ': 'county',
    'Район': 'district',
    'Метро': 'metro',
    'Способ передвижения': 'travel_type',
    'Время до метро (мин)': 'travel_time',
    'Категория': 'category',
    'Количество просмотров': 'views_count',
    'Количество фотографий': 'photos_count',
    'Этаж': 'floor_number',
    'Этажей в доме': 'floors_count',
    'Тип квартиры': 'flat_type',
    'Тип продажи': 'sale_type',
    'Количество отзывов': 'review_count',
    'Общий рейтинг': 'total_rate',
    'Тип проекта': 'project_type',
    'Апартаменты': 'is_apartment',
    'Пентхаус': 'is_penthouse',
    'Ипотека разрешена': 'is_mortgage_allowed',
    'Премиум': 'is_premium',
    'Экстренная продажа': 'is_emergency',
    'Программа реновации': 'renovation_programm',
    'Тип ремонта': 'repair_type',
    'Общая площадь (м²)': 'total_area',
    'Жилая площадь (м²)': 'living_area',
    'Площадь кухни (м²)': 'kitchen_area',
    'Высота потолков (м)': 'ceiling_height',
    'Количество балконов': 'balconies',
    'Количество лоджий': 'loggias',
    'Количество комнат': 'rooms_count',
    'Раздельный санузел': 'separated_wc',
    'Совмещённый санузел': 'combined_wc',
    'Год постройки': 'build_year',
    'Тип материала': 'material_type',
    'Мусоропровод': 'garbage_chute',
    'Количество лифтов': 'passenger_lifts',
    'Расстояние до центра (км)': 'distance_from_center',
    'Год': 'year',
    'Месяц': 'month',
    'День недели': 'day_of_week',
    'День месяца': 'day_of_month',
    'Стоимость': 'price'
}

column_order = [
    "Стоимость",
    "Общая площадь (м²)",
    "Жилая площадь (м²)",  
    "Площадь кухни (м²)",  
    "Количество комнат",  
    "Этаж",  
    "Этажей в доме",  
    "Год постройки", 
    "Метро",  
    "Время до метро (мин)",
    "Округ", 
    "Район",  
    "Тип квартиры", 
    "Тип материала", 
    "Тип ремонта",
    "Способ передвижения", 
    "Категория", 
    "Количество просмотров", 
    "Количество фотографий",  
    "Общий рейтинг", 
    "Ипотека разрешена",  
    "Премиум", 
    "Экстренная продажа", 
    "Программа реновации",  
    "Пентхаус", 
    "Апартаменты", 
    "Количество балконов",
    "Количество лоджий",
    "Мусоропровод",
    "Количество лифтов",
    "Расстояние до центра (км)"
]

def map_values(material_type, flat_type, repair_type, travel_type):
    return {
        "material_type": value_mappings["material_type"].get(material_type, material_type),
        "flat_type": value_mappings["flat_type"].get(flat_type, flat_type),
        "repair_type": value_mappings["repair_type"].get(repair_type, repair_type),
        "travel_type": value_mappings["travel_type"].get(travel_type, travel_type), 
    }

def map_dataframe(df, direction):
    if direction not in {"to_english", "to_russian"}:
        raise ValueError("Invalid direction. Use 'to_english' or 'to_russian'.")

    if direction == "to_english":
        df = df.rename(columns=column_mapping)

    for column in df.columns:
        if column in value_mappings:
            mapping = value_mappings[column]

            if direction == "to_english":
                selected_mapping = mapping
            else:
                reverse_mapping = {v: k for k, v in mapping.items()}
                selected_mapping = reverse_mapping

            df[column] = df[column].map(selected_mapping).fillna(df[column])
    
    if direction == "to_russian":
        reversed_column_mapping = {value: key for key, value in column_mapping.items()}
        df = df.rename(columns=reversed_column_mapping)
    return df

def reorder_columns(df):
    valid_columns = [col for col in column_order if col in df.columns]
    remaining_columns = [col for col in df.columns if col not in valid_columns]
    new_column_order = valid_columns + remaining_columns
    
    return df[new_column_order]

