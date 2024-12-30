import pandas as pd
import pickle
import math

with open('model/model.pickle', 'rb') as file:
    model_data = pickle.load(file)


def distance_from_center(data) -> pd.DataFrame:
    data['lat'] = data['coordinates'].apply(lambda x: x['lat'] if isinstance(x, dict) else None)
    data['lng'] = data['coordinates'].apply(lambda x: x['lng'] if isinstance(x, dict) else None)
    center_lat = 55.753600
    center_lng = 37.621184
    earth_radius_km = 6371

    def haversine(lat1, lng1, lat2, lng2):
        lat1, lng1, lat2, lng2 = map(math.radians, [lat1, lng1, lat2, lng2])
        dlat = lat2 - lat1
        dlng = lng2 - lng1
        a = math.sin(dlat / 2)**2 + math.cos(lat1) * \
            math.cos(lat2) * math.sin(dlng / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return earth_radius_km * c
    data['distance_from_center'] = data\
        .apply(lambda row: haversine(row['lat'], row['lng'], center_lat, center_lng), axis=1)
    return data


def preparams(data) -> dict:
    tables = {
        "addresses": [],
        "developers": [],
        "offers": [],
        "offers_details": [],
        "realty_details": [],
        "realty_inside": [],
        "realty_outside": []}

    for table_name in tables.keys():
        if hasattr(data, table_name):
            tables[table_name].append(getattr(data, table_name).dict())

    dfs = {table: pd.DataFrame(tables[table]) for table in tables}

    data = dfs["addresses"].merge(dfs["offers"], on='cian_id', how='inner')\
        .merge(dfs["offers_details"], on='cian_id', how='inner')

    tables_to_left_join = [dfs["developers"], dfs["realty_details"],
                           dfs["realty_inside"], dfs["realty_outside"]]
    for table in tables_to_left_join:
        data = data.merge(table, on='cian_id', how='left')

    # расчитываем дистанцию от центра
    data = distance_from_center(data)
    return data.iloc[0].to_dict()


def preprepict(data) -> pd.DataFrame:
    data = pd.DataFrame([data.dict()])
    data['lat'] = data['coordinates'].apply(lambda x: x['lat'] if isinstance(x, dict) else None)
    data['lng'] = data['coordinates'].apply(lambda x: x['lng'] if isinstance(x, dict) else None)
    data.drop(columns=['coordinates'], inplace=True)

    data['publication_at'] = pd.to_datetime(pd.to_datetime(data['publication_at'], unit='s', utc=True).dt.date)

    data['finish_year'] = data['finish_date'].apply(lambda x: x.get('year') if isinstance(x, dict) else None)

    data['realty_type'] = data['realty_type'].replace('none', None)
    data.loc[data['finish_year'] <= 0, 'finish_year'] = None
    data['material_type'] = data['material_type'].replace('none', None)
    data.drop(columns=['finish_date'], inplace=True)

    data['total_rate'] = data['total_rate'].astype(float).fillna(4.180479743602584)
    data['review_count'] = data['review_count'].astype(float).fillna(1248.7316089939407)

    mean_proportion_ceiling_height = 0.06049278161032404
    formula = data['total_area'] * mean_proportion_ceiling_height
    data['ceiling_height'] = data['ceiling_height'].where(data['ceiling_height'] > 0, formula)

    mean_proportion_living_area = 0.5486437974462534
    data['living_area'] = data['living_area'].astype(float).fillna(data['total_area'] * mean_proportion_living_area)

    mean_proportion_kitchen_area = 0.4577734591774278
    mask = (data['total_area'] - data['living_area']
            ).replace(0, pd.NA) * mean_proportion_kitchen_area
    data['kitchen_area'] = data['kitchen_area'].astype(float).fillna(mask)
    mean_proportion_rooms_count = 0.06657494706605477
    data['rooms_count'] = data['rooms_count']\
        .fillna(data['living_area'] * mean_proportion_rooms_count).astype(int)
    data['build_year'] = data\
        .apply(lambda row: row['finish_year'] if pd.isna(row['build_year']) else row['build_year'], axis=1)

    data['separated_wc'] = data['separated_wc'].astype(float).fillna(0)
    data['loggias'] = data['loggias'].astype(float).fillna(0)
    data['balconies'] = data['balconies'].astype(float).fillna(0)
    data['combined_wc'] = data['combined_wc'].astype(float).fillna(0)
    data['passenger_lifts'] = data['passenger_lifts'].astype(float).fillna(0)

    data['is_penthouse'] = data['is_penthouse'].astype(bool).fillna(False)
    data['garbage_chute'] = data['garbage_chute'].astype(bool).fillna(False)
    data['is_emergency'] = data['is_emergency'].astype(bool).fillna(False)
    data['is_apartment'] = data['is_apartment'].astype(bool).fillna(False)
    data['is_mortgage_allowed'] = data['is_mortgage_allowed'].astype(bool).fillna(False)
    data['renovation_programm'] = data['renovation_programm'].astype(bool).fillna(False)
    data['is_premium'] = data['is_premium'].astype(bool).fillna(False)
    data['views_count'] = data['views_count'].fillna(632)
    data['photos_count'] = data['photos_count'].fillna(18)
    data['material_type'] = data['material_type'].fillna('panel')
    data['repair_type'] = data['repair_type'].fillna('cosmetic')
    data['project_type'] = data['project_type'].fillna('Индивидуальный проект')
    data['category'] = data['category'].fillna('flatSale')
    data['sale_type'] = data['sale_type'].fillna('free')

    columns_to_int = [
        'price', 'travel_time', 'views_count', 'balconies', 'loggias', 'photos_count',
        'separated_wc', 'combined_wc', 'passenger_lifts', 'review_count', 'build_year'
    ]

    for col in columns_to_int:
        data[col] = data[col].apply(lambda x: int(x) if pd.notna(x) else None)

    data['publication_at'] = pd.to_datetime(data['publication_at'])
    data['year'] = data['publication_at'].dt.year
    data['month'] = data['publication_at'].dt.month
    data['day_of_week'] = data['publication_at'].dt.dayofweek
    data['day_of_month'] = data['publication_at'].dt.day

    data = data.drop(columns=['publication_at'])
    return data


def encoding(data) -> pd.DataFrame:
    # onehot
    onehot_columns = model_data['onehot_encoder'].feature_names_in_
    for col in onehot_columns:
        if col not in data.columns:
            return ValueError(f"Признак '{col}' отсутствует в данных")
        if data[col].isnull().any():
            return ValueError(f"Признак '{col}' пустой")
    data_encoded = pd.DataFrame(model_data['onehot_encoder'].transform(data[onehot_columns]),
                                columns=model_data['onehot_encoder'].get_feature_names_out(onehot_columns))
    data = pd.concat([data.drop(columns=onehot_columns).reset_index(drop=True), data_encoded], axis=1)

    # origin
    if data.get('repair_type') is None:
        return ValueError("Признак 'repair_type' пустой")
    orignal_columns = {'repair_type': {'no': 0, 'cosmetic': 1, 'euro': 2, 'design': 3}}
    for col, mapping in orignal_columns.items():
        data[col] = data[col].map(mapping)

    # target
    target_columns = ['district', 'project_type', 'metro']
    for col in target_columns:
        if col not in data.columns:
            return ValueError(f"Признак '{col}' отсутствует в данных")
        if data[col].isnull().any():
            return ValueError(f"Признак '{col}' пустой")
    data[target_columns] = pd.DataFrame(model_data['target_encoder'].transform(data[target_columns]),
                                        columns=target_columns)

    # scaler
    scaler_columns = model_data['scaler'].feature_names_in_
    for col in scaler_columns:
        if col not in data.columns:
            return ValueError(f"Признак '{col}' отсутствует в данных")
        if data[col].isnull().any():
            return ValueError(f"Признак '{col}' пустой")
    data = data[scaler_columns]
    data = pd.DataFrame(model_data['scaler'].transform(data), columns=data.columns)

    # model
    model_columns = [col for col in model_data['model'].feature_names_in_ if col in data.columns]
    for col in model_columns:
        if col not in data.columns:
            return ValueError(f"Признак '{col}' отсутствует в данных")
        if data[col].isnull().any():
            return ValueError(f"Признак '{col}' пустой")
    data = data[model_columns]
    return data


def prediction(data) -> float:
    # predict
    predict = model_data['model'].predict(data)
    return predict[0]
